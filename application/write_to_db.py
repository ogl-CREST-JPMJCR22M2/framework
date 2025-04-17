### partidを使って求める

from sqlalchemy import create_engine
import polars as pl
from psycopg2 import connect, sql
from psycopg2.extras import execute_values
import SQLexecutor as SQLexe



### irohaに渡すためのデータ加工

def to_iroha(df):

    part_list = df["partid"].to_list()
    hash_list = df["hash"].to_list()

    return part_list, hash_list


### offchaindbのcfpの更新

def update_cfp_to_off(peer, target_part, cfp = None, sabun = None):

    if sabun != None and cfp == None:

        sql_statement = sql.SQL(
            """
            UPDATE cfpval set totalcfp = {sabun} + totalcfp where partid = {target_part};
            """
        ).format(
            target_part = sql.Literal(target_part),
            sabun = sql.Literal(sabun)
        )

    elif sabun != None and cfp != None:

        sql_statement = sql.SQL(
            """
            UPDATE cfpval set (totalcfp, cfp) = (totalcfp + {sabun}, {cfp}) where partid = {target_part};
            """
        ).format(
            target_part = sql.Literal(target_part),
            sabun = sql.Literal(sabun),
            cfp = sql.Literal(cfp)
        )

    SQLexe.COMMANDexecutor_off(sql_statement, peer)


### まとめてhashをUPSERT

def upsert_hash_exe(df, peer):

    upsert_sql = """
        INSERT INTO merkle_tree (partid, hash)
        VALUES %s
        ON CONFLICT (partid) DO UPDATE SET hash = EXCLUDED.hash;
    """

    # DB接続
    conn = connect(
        dbname = "iroha_default", 
        user = "postgres", 
        password = "mysecretpassword",
        host = "postgres" + peer,
        port = 5432
    )

    with conn.cursor() as cur:
        data = df.select(["partid", "hash"]).rows()
        execute_values(cur, upsert_sql, data)

    conn.commit()
    conn.close()



### 一回だけhashをUPSERT

def upsert_hash(partid, hash_val, peer):

    upsert_sql = sql.SQL( """
        INSERT INTO merkle_tree (partid, hash)
        VALUES ({partid}, {hash_val})
        ON CONFLICT (partid) DO UPDATE SET hash = {hash_val};
    """
    ).format(
            partid = sql.Literal(partid),
            hash_val = sql.Literal(hash_val)
    )

    SQLexe.COMMANDexecutor_on(upsert_sql, peer)
    

