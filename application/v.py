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


def valification(peer, root_partid):

    peers = ["postgresA", "postgresB", "postgresC"]

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
                    cfp DECIMAL, 
                    hash CHARACTER varying(64),
                    new_hash CHARACTER varying(64),
                    PRIMARY KEY (partid)
                );
            """)

            ## cfpの算出
            # offchain-dbからcfpの算出
            cfp_import = " UNION ALL \n".join(["SELECT * FROM dblink('host="+ p +" port=5432 dbname=offchaindb user=postgres password=mysecretpassword', 'SELECT partid, cfp FROM cfpval') AS t1(partid CHARACTER varying(288), cfp DECIMAL)" 
            for p in peers ]) 
        
            sql_ = f"""
                INSERT INTO temp (partid, parents_partid, priority, cfp, hash, new_hash) 
                WITH plain_totalcfp AS (
                    {cfp_import}
                ),
                part_tree AS( 
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
                        SELECT calc.partid, parents_partid, priority, cfp, hash, 'null'
                        FROM  calc, plain_totalcfp pt, hash_parts_tree m
                        WHERE calc.partid = pt.partid AND calc.partid = m.partid
                )
                SELECT * FROM part_tree;

                UPDATE temp SET new_hash = encode(digest(cfp::TEXT, 'sha256'), 'hex')
                    WHERE NOT EXISTS (SELECT parents_partid FROM partrelationship WHERE partrelationship.parents_partid = temp.partid);

                SELECT * FROM temp WHERE new_hash = 'null'
            """
            cur.execute(sql_, (root_partid,))
            
            not_hashed = cur.fetchall()

            while len(not_hashed) > 0: 

                sql_2 = """ 
                    WITH can_hashing AS (
                        SELECT parents_partid, bool_and(new_hash != 'null') as result FROM temp
                        Group by parents_partid
                    )
                    SELECT temp.parents_partid, array_agg(new_hash)
                    FROM can_hashing, temp
                    WHERE result = True AND can_hashing.parents_partid = temp.parents_partid
                    Group by temp.parents_partid;
                """ 
                cur.execute(sql_2)
                queue = cur.fetchall()

                for q in queue:
                    xor_hashed = xor_hash(q[1])

                    sql_32 = f"UPDATE temp SET new_hash = encode(digest( encode(digest(cfp::TEXT, 'sha256'), 'hex')||'{xor_hashed}' ::TEXT, 'sha256'), 'hex') WHERE partid = %s"
                    cur.execute(sql_32,  (q[0],))
                
                # 終了条件のアップデート
                sql_4 = "SELECT * FROM temp WHERE new_hash = 'null';"
                cur.execute(sql_4)
                not_hashed = cur.fetchall()

            sql_5 = """
            WITH valification AS (
                SELECT partid, hash != new_hash as result FROM temp
            )
            SELECT partid FROM valification WHERE result = 'False';
            """
            cur.execute(sql_5)
            data = cur.fetchall()

    finally:
        if conn:
            conn.close()
    
    return data


# ======== MAIN ======== #

if __name__ == '__main__':

    root_partid = 'P0'
    assembler = w.get_Assebler(root_partid)

    start = time.time()

    result = valification(assembler, root_partid)

    if len(result) == 0:
        print("varification successfully")
    else:
        print(result)
    
    t = time.time() - start
    print("time:", t)
