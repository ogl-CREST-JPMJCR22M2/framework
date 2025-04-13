### マークルツリーで検証を行う

from sqlalchemy import create_engine
import calculation as cal
import polars as pl
import time

# onchain-dbに接続，merkle treeのdetaframeを取得

def get_hash_df(peer):

    engine = create_engine("postgresql://postgres:mysecretpassword@postgres"+peer+":5432/iroha_default")

    sql_statement =" SELECT partid, hash FROM totalcfpval;"

    df = pl.read_database(sql_statement, engine)
    
    return df


# 既存のhashval(onchain-dbから取得)とアンチ結合を使うことで比較

def varification(df_pre, df_new):

    df_joined = df_new.join(df_pre, on = "hash", how = "anti")

    if len(df_joined) == 0:
        print("Verification Successfully")
    else:
        print("Verification failed")
        print(df_joined["partid"])
    
    return


if __name__ == '__main__':

    root_partid = "P0"

    varification(get_hash_df("A"), cal.make_merkltree(root_partid))
