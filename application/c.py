### partidを使って求める

from sqlalchemy import create_engine, text
import polars as pl
import time
import hashlib
from decimal import *
import zlib
from typing import Optional
from psycopg2 import connect, sql
from psycopg2.extras import execute_values
from psycopg2._psycopg import connection, cursor
from collections import defaultdict

import SQLexecutor as SQLexe
import write_to_db as w


# ======== DataFrameの表示の仕方 ======== #
pl.Config.set_tbl_cols(-1)
pl.Config.set_tbl_rows(-1)
pl.Config.set_fmt_str_lengths(n=30)
# ===================================== #


def xor_hash(strings):
    result = bytearray(32)  # SHA-256は32バイト（256ビット）
    for s in strings:
        h = bytes.fromhex(s)
        for i in range(32):
            result[i] ^= h[i]  # XOR 合成
    return result.hex()


def hash_part_tree(peer, peers, root_partid):

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
                CREATE TEMP TABLE temp (
                    partid CHARACTER varying(288),
                    parents_partid CHARACTER varying(288),
                    priority int,
                    assembler CHARACTER varying(288),
                    cfp DECIMAL, 
                    co2 DECIMAL,
                    hash CHARACTER varying(64),
                    PRIMARY KEY (partid)
                );

                CREATE TEMP TABLE cfpval(
                    partid CHARACTER varying(288),
                    co2 DECIMAL,
                    PRIMARY KEY (partid)
                );

                CREATE INDEX idx_temp_hash ON temp(hash);
            """)

            ## cfpの算出
            # offchain-dbからcfpの算出
            co2_import = " UNION ALL \n".join(["SELECT * FROM dblink('host="+ p +" port=5432 dbname=offchaindb user=postgres password=mysecretpassword', 'SELECT partid, co2 FROM cfpval') AS t1(partid CHARACTER varying(288), co2 DECIMAL)" 
            for p in peers ]) 
        
            sql_ = f"""
                INSERT INTO cfpval (partid, co2)
                {co2_import}

                INSERT INTO temp (partid, parents_partid, priority, assembler, cfp, co2, hash) 
                WITH part_tree AS( 
                    WITH RECURSIVE calc(partid, parents_partid, priority) AS 
                        ( 
                            SELECT partid, parents_partid, priority
                            FROM partrelationship r
                            WHERE partid = %s

                            UNION ALL 

                            SELECT r.partid, r.parents_partid, r.priority
                            FROM partrelationship r, calc 
                            WHERE r.parents_partid = calc.partid 
                        ) 
                        SELECT calc.partid, parents_partid, priority, co2 
                        FROM  calc, cfpval
                        WHERE calc.partid = cfpval.partid
                ), 
                get_cfp AS (
                    WITH RECURSIVE subtree_sum(root_id, current_id, co2) AS 
                        ( 
                            SELECT 
                            partid AS root_id, partid AS current_id, co2
                            FROM part_tree

                            UNION ALL 

                            SELECT ss.root_id, pt.partid AS current_id, pt.co2
                            FROM subtree_sum ss, part_tree pt
                            WHERE pt.parents_partid = ss.current_id 
                        ) 
                        SELECT 
                        root_id AS partid, SUM(co2) AS cfp
                        FROM subtree_sum
                        GROUP BY root_id
                )
                SELECT pt.partid, parents_partid, priority, assembler, cfp, co2, 'null'
                FROM part_tree pt, get_cfp gt, partinfo i
                WHERE pt.partid = gt.partid AND pt.partid = i.partid;

                UPDATE temp SET hash = encode(digest(cfp::TEXT, 'sha256'), 'hex')
                    WHERE NOT EXISTS (SELECT parents_partid FROM partrelationship WHERE partrelationship.parents_partid = temp.partid);

            """
            cur.execute(sql_, (root_partid,))
            
            not_hashed = cur.fetchall()
            not_hashed_list = []

            for partid in not_hashed:
                    not_hashed_list.append(partid)

            while len(not_hashed_list) > 0: 

                sql_2 = """
                    WITH can_hashing AS (
                        SELECT parents_partid, bool_and(hash != 'null') as result FROM temp
                        Group by parents_partid
                    )
                    SELECT temp.parents_partid AS partid, array_agg(hash) AS hash_list
                    FROM can_hashing, temp
                    WHERE result = True AND can_hashing.parents_partid = temp.parents_partid
                    Group by temp.parents_partid;
                """ 
                cur.execute(sql_2)
                queue = cur.fetchall()

                for partid, hash_list in queue:
                    xor_hashed = xor_hash(hash_list)

                    sql_32 = f"""
                        UPDATE temp SET hash = encode(digest( encode(digest(cfp::TEXT, 'sha256'), 'hex')||'{xor_hashed}' ::TEXT, 'sha256'), 'hex') 
                        WHERE partid = %s;
                    """
                    cur.execute(sql_32,  (partid,))
                
                # 終了条件のアップデート
                not_hashed_list = not_hashed_list - queue[0]

            sql_5 = "SELECT partid, assembler, cfp, hash as hashval FROM temp;"
            cur.execute(sql_5)
            data = cur.fetchall()

    finally:
        if conn:
            conn.close()
    
    return data


def make_merkltree(assembler, root_partid):

    peers = ["postgresA", "postgresB", "postgresC"]

    start = time.time()
    ## postgres処理
    result = hash_part_tree(assembler, peers, root_partid)

    print("ツリー構築",time.time()-start)
    start = time.time()

    # polarsに変換
    part_list = []
    hash_list = []

    # assemblerごとの2次元リスト (insert_val)
    insert_val_dict = defaultdict(list)

    for partid, assembler, cfp, hashval in result:
        part_list.append(partid)
        hash_list.append(hashval)
        insert_val_dict[assembler].append((partid, cfp))

    # assemblerごとのリストに変換
    #insert_val = list(insert_val_dict.values())
    # ↑の辞書のkey
    assembler_unique = list(insert_val_dict.keys())

    print("データの抽出",time.time()-start)
    start = time.time()

    # Irohaコマンドで書き込み
    SQLexe.IROHA_CMDexe(assembler, part_list, hash_list)

    print("iroha実行",time.time()-start)
    start = time.time()

    # offchain-dbへの書き込み
    for key in assembler_unique:

        upsert_sql = """
            UPDATE cfpval AS t
            SET
                partid = v.partid,
                cfp = v.cfp
            FROM (VALUES %s)
            AS v(partid, cfp)
            WHERE v.partid = t.partid;
        """

        # DB接続
        conn = connect(
            dbname = "offchaindb", 
            user = "postgres", 
            password = "mysecretpassword",
            host = key,
            port = 5432
        )

        with conn.cursor() as cur:
            execute_values(cur, upsert_sql, insert_val_dict[key])

        conn.commit()
        conn.close()

    print("offchainへwrite",time.time()-start)


# ======== MAIN ======== #

if __name__ == '__main__':

    root_partid = 'P0'
    assembler = w.get_Assebler(root_partid)

    start = time.time()

    make_merkltree(assembler, root_partid)
    
    t = time.time() - start
    print("time:", t)
