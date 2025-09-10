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

from collections import defaultdict, deque
from psycopg2.extras import RealDictCursor

# XORユーティリティ
def xor_bytes(*args: bytes) -> bytes:
    result = bytearray(32)
    print(result)
    for b in args:
        print(b)
        for i in range(32):
            print(result[i],"|", b[i])
            result[i] ^= b[i]
    return bytes(result)

def xor_sha256_list(lst):
    if not lst:
        return bytes(32)
    res = lst[0]
    for b in lst[1:]:
        res = xor_bytes(res, b)
    return res


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
        cur = conn.cursor(cursor_factory=RealDictCursor)

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
                CREATE INDEX idx_hash_val ON hashvals(hash);
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
            co2_import = " UNION ALL \n".join(["SELECT * FROM dblink('host="+ p +" port=5432 dbname=offchaindb user=postgres password=mysecretpassword', 'SELECT partid, cfp FROM cfpval') AS t1(partid CHARACTER varying(288), cfp DECIMAL)" 
            for p in peers ]) 
        

            sql_2 = f"""
                -- cfp算出
                INSERT INTO calc_cfp (partid, cfp, hash_cfp) 
                WITH cfpvals AS (
                    {co2_import}
                )
                SELECT DISTINCT cv.partid, cfp, digest(cfp::text, 'sha256') AS hash_cfp
                FROM cfpvals cv, target_tree tt
                WHERE cv.partid = tt.partid;

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
                SELECT DISTINCT
                        h.parents_partid AS partid,
                        h.partid AS child_partid, 
                        h.duplication,
                        hv.hash AS parent_base,
                        h.hash AS child_hash,
                        decode(hpt2.hash,'hex') AS correct_parent_hash,
                        decode(hpt.hash,'hex') AS correct_child_hash
                    FROM hashvals h
                    JOIN hash_parts_tree hpt ON h.partid = hpt.partid
                    LEFT JOIN hashvals hv ON h.parents_partid = hv.partid
                    LEFT JOIN hash_parts_tree hpt2 ON h.parents_partid = hpt2.partid
                    WHERE hpt.hash <> encode(h.hash, 'hex');
            """)
            
            edges = cur.fetchall()

            # 2) データ構造に整形
            children_map = defaultdict(list)
            parent_base_map = dict()
            correct_parent_map = dict()
            dup_map = dict()
            child_hash_map = dict()
            correct_child_map = dict()

            for e in edges:
                parent = e[0]
                child  = e[1]
                dup_map[(parent, child)] = e[2]
                children_map[parent].append(child)
                parent_base_map[parent] = e[3]
                child_hash_map[(parent, child)] = e[4]
                correct_parent_map[parent] = e[5]
                correct_child_map[(parent, child)] = e[6]


            # 3) 葉→親→祖先の順で復元
            restored_hash_map = dict()
            tampered_flags = dict()
            processed = set()

            # 葉を含む全ノード
            all_parents = set(parent_base_map.keys())
            all_children = set(child_hash_map.keys())
            leaf_candidates = all_children - all_parents

            # キューで階層ごとに処理
            queue = deque(all_parents)  # 全親を順次処理

            while queue:
                parent = queue.popleft()
                if parent in processed:
                    continue
                childs = children_map.get(parent, [])
                # 子の復元値がまだ計算されていない場合は後回し
                if any(c in children_map and c not in processed for c in childs):
                    queue.append(parent)
                    continue
                delta_list = []
                for child in childs:
                    ch_hash = child_hash_map[(parent, child)]
                    correct_ch = correct_child_map[(parent, child)]
                    if ch_hash != correct_ch:
                        delta_list.append(xor_bytes(ch_hash, correct_ch))
                        tampered_flags[(parent, child)] = True
                    else:
                        delta_list.append(bytes(32))
                        tampered_flags[(parent, child)] = False
                parent_base = parent_base_map[parent]
                parent_restored = xor_sha256_list([parent_base] + delta_list)
                restored_hash_map[parent] = parent_restored
                processed.add(parent)
                # この親の上位ノードがあればキューに追加
                for p, children in children_map.items():
                    if parent in children and p not in processed:
                        queue.append(p)

            # 4) 結果出力
            for parent, childs in children_map.items():
                for child in childs:
                    print(f"Parent: {parent}, Child: {child}, "
                        f"Restored: {restored_hash_map[parent].hex()}, "
                        f"Correct: {correct_parent_map[parent].hex()}, "
                        f"Tampered: {tampered_flags[(parent, child)]}")

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
        #print(result)
        print("varification faild")
    
    t = time.time() - start
    print("time:", t)

