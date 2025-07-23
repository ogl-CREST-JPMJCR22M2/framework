### partidを使って求める

import time
import hashlib
from decimal import *
from typing import Optional
from psycopg2 import connect, sql
from psycopg2._psycopg import connection, cursor
from psycopg2.extras import execute_values

import SQLexecutor as SQLexe
import write_to_db as w


def valification(peer, peers, root_partid):

    conn: Optional[connection] = None
    try:
        dsn = {
            "dbname": "iroha_default",
            "user": "postgres",
            "password": "mysecretpassword",
            "port": "5432",
            "host": peer
        }
        conn = connect(**dsn)
        conn.autocommit = True

        with conn.cursor() as cur:

            ## 一時テーブルの構築
            cur.execute("""
                CREATE TEMP TABLE target_tree (
                    partid CHARACTER varying(288),
                    parents_partid CHARACTER varying(288),
                    qty int,
                    UNIQUE (partid, parents_partid)
                );
                
                CREATE TEMP TABLE calc_cfp (
                    partid CHARACTER varying(288),
                    cfp DECIMAL, 
                    hash_cfp bytea,
                    PRIMARY KEY (partid)
                );

                CREATE TEMP TABLE hashvals(
                    partid CHARACTER varying(288),
                    parents_partid CHARACTER varying(288),
                    can_hashing boolean,
                    duplication boolean,
                    hash bytea,
                    UNIQUE (partid, parents_partid)
                );

                CREATE INDEX idx_tree ON target_tree(partid);
                CREATE INDEX idx_cfp ON calc_cfp(partid);
                CREATE INDEX idx_hash ON hashvals(partid);
            """)
            
            # 部品木の抽出
            sql_1 = f"""
                INSERT INTO target_tree (partid, parents_partid, qty) 
                    WITH RECURSIVE get_tree(partid, parents_partid) AS 
                        ( 
                            SELECT partid, parents_partid, qty
                            FROM partrelationship
                            WHERE partid = %s

                            UNION

                            SELECT r.partid, r.parents_partid, r.qty
                            FROM partrelationship r, get_tree gt
                            WHERE r.parents_partid = gt.partid 
                        )
                        SELECT gt.partid, gt.parents_partid, qty
                        FROM get_tree gt;
                """
            cur.execute(sql_1, (root_partid, ))

            ## cfpの算出
            # offchain-dbからcfpの算出
            co2_import = " UNION ALL \n".join(["SELECT * FROM dblink('host="+ p +" port=5432 dbname=offchaindb user=postgres password=mysecretpassword', 'SELECT partid, co2 FROM cfpval') AS t1(partid CHARACTER varying(288), co2 DECIMAL)" 
            for p in peers ]) 
        

            sql_2 = f"""
                -- cfp算出
                INSERT INTO calc_cfp (partid, cfp, hash_cfp) 
                WITH co2vals AS (
                    {co2_import}
                ),
                cfpvals AS(               
                    WITH RECURSIVE calc_qty(partid, root, quantity) AS (
                        SELECT DISTINCT
                            tt.partid,
                            tt.partid AS root,
                            1::BIGINT AS quantity
                        FROM target_tree tt

                        UNION ALL

                        SELECT
                            tt.partid,          -- 子部品
                            cq.root,           -- スタート部品は固定
                            cq.quantity * tt.qty -- 親の個数 * 使用数（qty）
                        FROM calc_qty cq
                        JOIN target_tree tt ON tt.parents_partid = cq.partid
                    )
                    SELECT
                        cq.root AS partid,
                        ROUND(SUM(c.co2 * cq.quantity), 4) AS cfp
                    FROM calc_qty cq
                    JOIN co2vals c ON cq.partid = c.partid
                    GROUP BY cq.root
                    ORDER BY cq.root
                )
                SELECT partid, cfp, digest(cfp::text, 'sha256') AS hash_cfp
                FROM cfpvals;

            """
            cur.execute(sql_2)

            # 単品部品の処理
            sql_3 = f"""
                INSERT INTO hashvals (partid, parents_partid, can_hashing, duplication, hash)
                    WITH check_duplication AS (
                        SELECT partid, COUNT(partid) > 1 AS duplication
                        FROM target_tree
                        GROUP BY partid
                    )
                    SELECT 
                        tt.partid, tt.parents_partid,
                        -- ハッシュ化可能か
                        CASE 
                            WHEN EXISTS ( SELECT 1 FROM target_tree tt WHERE tt.parents_partid = calc_cfp.partid ) THEN False
                            ELSE True
                        END AS can_hashing,
                        -- 重複チェック
                        duplication,
                        hash_cfp AS hash
                    FROM calc_cfp, target_tree tt, check_duplication cd
                    WHERE calc_cfp.partid = tt.partid AND tt.partid = cd.partid;
            """
            cur.execute(sql_3)

            while True: 

                # 終了条件
                cur.execute("SELECT partid FROM hashvals WHERE can_hashing = False LIMIT 1;")
                row = cur.fetchone()

                if not row:
                    break

                sql_4 = """
                    WITH get_can_hashing AS (
                        SELECT 
                            parents_partid, 
                            bool_and(can_hashing)
                        FROM hashvals
                        GROUP BY parents_partid 
                        HAVING bool_and(can_hashing) = True
                    ), 

                    check_dup AS (
                        SELECT partid AS partid_org, gch.parents_partid AS partid,
                            CASE duplication 
                                WHEN True THEN digest( hash::text || gch.parents_partid::text, 'sha256')
                                ELSE hash
                            END AS hash_under_calc
                        FROM get_can_hashing gch, hashvals h
                        WHERE gch.parents_partid = h.parents_partid
                    ),

                    hashing AS (
                        SELECT 
                            partid,
                            array_agg(hash_under_calc) AS hash_list
                        FROM check_dup
                        GROUP BY partid 
                    )

                    UPDATE hashvals SET (can_hashing, hash) = (True, xor_sha256(hash_list || hash)) 
                    FROM hashing h
                    WHERE h.partid = hashvals.partid AND can_hashing = False;
                """ 
                cur.execute(sql_4)

            # 検証

            sql_5 = f"""
                SELECT hpt.hash = encode(hashvals.hash, 'hex') AS result
                    FROM hashvals, hash_parts_tree hpt
                    WHERE hashvals.partid = hpt.partid AND hpt.partid = %s;
            """
            cur.execute(sql_5, (root_partid, ))
            row = cur.fetchone()
            

            if row[0] == True : return True # 出力がない = 検証成功

            ## 特定処理続行

            cur.execute("""
                CREATE TEMP TABLE path(
                    partid CHARACTER varying(288),
                    parents_partid CHARACTER varying(288),
                    hash bytea,
                    hash_on bytea,
                    hash_kensho bytea,
                    UNIQUE (partid, parents_partid)
                );

                CREATE INDEX idx_path ON path(partid);

                INSERT INTO path (partid, parents_partid, hash, hash_on)
                    SELECT 
                        h.partid, 
                        h.parents_partid,
                        h.hash, 
                        decode(hpt.hash, 'hex') AS hash_on
                    FROM hashvals h, hash_parts_tree hpt
                    WHERE h.partid = hpt.partid AND hpt.hash <> encode(h.hash, 'hex');

                SELECT partid FROM path WHERE partid NOT IN (SELECT parents_partid FROM path);
            """)
            target = cur.fetchall()

            kaizan_kamo = set()
            
            while True:
                ## 検証失敗のため特定処理へ
                # 初期値点ごとで繰り返し
                for n in target:

                    now_searching = n[0]
                    kaizan_kamo.add(now_searching)

                    cur.execute(f"""
                        WITH target_hash AS (
                            SELECT xor_sha256(ARRAY[hash, hash_on]) AS xor_hash 
                            FROM path 
                            WHERE partid = '{now_searching}'
                        ),
                        do_xor AS (
                            WITH RECURSIVE xor_leaf(partid, parents_partid) AS (
                                SELECT partid, parents_partid, hash_on AS done_xor_hash
                                FROM path
                                WHERE partid = '{now_searching}'

                                UNION

                                SELECT p.partid, p.parents_partid, xor_sha256(ARRAY[hash, xor_hash]) AS done_xor_hash
                                FROM path p, target_hash, xor_leaf
                                WHERE p.partid = xor_leaf.parents_partid
                            )
                            SELECT partid, done_xor_hash
                            FROM xor_leaf
                        )
                        UPDATE path SET hash = done_xor_hash
                        FROM do_xor dx
                        WHERE dx.partid = path.partid;
                    """)
                
                # 検証

                cur.execute("""
                    WITH checking AS (
                        SELECT partid, parents_partid, hash = hash_on AS result
                        FROM path
                    ),
                    false_list AS (
                        SELECT partid, parents_partid 
                        FROM checking 
                        WHERE result = False
                    )
                    SELECT partid 
                    FROM false_list 
                    WHERE partid NOT IN (SELECT parents_partid FROM false_list);
                """)
                target = cur.fetchall()  

                if len(target) == 0 : break # 出力がない = 検証成功

    finally:
        if conn:
            conn.close()
    
    return kaizan_kamo

# ======== MAIN ======== #

if __name__ == '__main__':

    root_partid = 'P0'
    peers = ["postgresA", "postgresB", "postgresC"]

    assembler = w.get_Assebler(root_partid)

    start = time.time()

    result = valification(assembler, peers, root_partid)

    if result == True:
        print("varification successfully")
    else:
        print(result)
        print(len(result))
    
    t = time.time() - start
    print("time:", t)

