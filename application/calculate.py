import pandas as pd
import SQLexecutor as SQLexe
from psycopg2 import sql
from sqlalchemy import create_engine
import commons as com
import polars as pl
import time

# offchainに接続，cfpをget
def get_cfpval(peer):

    engine = create_engine("postgresql://postgres:mysecretpassword@postgres"+peer+":5432/offchaindb")

    sql_statement =" SELECT partid, cfp FROM cfpval;"

    df = pl.read_database(sql_statement, engine)
    
    return df


# offchainから全てのcfpをget，結合
def join_cfpvals(peer):

    df1 = get_cfpval(peer[0])

    for p in peer[1:]:
        df2 = get_cfpval(p)
        df1 = pl.concat([df1, df2])

    return df1

# 部品木全体を取得
def get_tree(peer):

    engine = create_engine("postgresql://postgres:mysecretpassword@postgres"+peer+":5432/iroha_default")

    sql_statement ="SELECT partid, parents_partid FROM partrelationship;"

    all_tree = pl.read_database(sql_statement, engine)

    return all_tree

# 部品木を抽出
def get_childpart(df, parents_partid):

    child_df = df.filter(pl.col("parents_partid") == parents_partid)

    childpart = child_df["partid"].to_list()
    
    for child in childpart:
        child_df = pl.concat([child_df, get_childpart(df, child)])

    return child_df
    

def get_hash(df, target_id):

    df = df.with_row_index()
    df = 



    return hashed

if __name__ == '__main__':

    peer = "A"
    partid = 'P0'
    start = time.time()
    df = get_childpart(get_tree(peer), partid)
    print(get_hash(df, partid))
    t = time.time() - start
    print(t)


def calc_totaocfp(partid, peer, cfp):

    # pandaframeに格納
    # totalcfp算出

    SQL = sql.SQL("""

            UPDATE cfpval set totalcfp = {totalcfp} 
            WHERE partid = {partid} ;

        """).format(
            partid = sql.Literal(partid),
            cfp = sql.Literal(cfp)
        )

    SQLexe.COMMANDexecutor_off(SQL, peer)

