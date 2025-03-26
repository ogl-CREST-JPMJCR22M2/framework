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
    
# ハッシュ化    
def hash_data(self, data):
        return hashlib.sha256(data.encode()).hexdigest()

def get_hash(df, target_id):

    # 動作確認の値セット  
    df_h = pl.DataFrame(
        {
            "partid" : ["P"+str(i) for i in range(1, 156)],
            "part_hash" : ["H"+str(i) for i in range(1, 156)],
            #"part_hash" : ["h"+str(i) for i in range(1, 156)],
        }
    )

    df = df.join(df_h, on=["partid"], how="left")

    #葉ノードの抽出
    parent_counts = df["parents_partid"].value_counts().rename({"parents_partid": "partid"})
    df = df.join(parent_counts, on=["partid"], how="left").fill_null(0)


    #ハッシュの算出
    #df = df.with_columns(
    #    pl.col("partid").hash().alias("cfpval_hash")
    #)  

    #葉ノードには hash ← part_hash
    
    df = df.with_columns(
        pl.when(pl.col("count") != 0)
        .then(pl.lit(float("NAN")))  # NaN を代入
        .otherwise(pl.col("part_hash"))  # それ以外は元の値を保持
        .alias("hash")  # カラム名を指定
    ) 

    #葉ノードをキューに追加

    sorted_parts = []
    processing_queue = df.filter(pl.col("count") == 0)["partid"].to_list()

    while processing_queue:
        
        part = processing_queue.pop(0)  # 先頭を処理

        parenttpart = df.filter(pl.col("partid") == part)["parents_partid"].to_list() # 先頭partの親部品の取得

        if not parenttpart : break # ルート部品ならbreak

        df.filter(pl.col("partid") == part)["part_hash"].item()

        #hashed_part = parenttpart[0] + part

        c = parent_counts.filter(pl.col("partid") == parenttpart[0])["count"].item() # 子部品数の取得

        
        
        for i in range(c-1):
            part = part + processing_queue.pop(0)
            
        part = "(" + part + ")"

        print(part)

        #親をキューに追加
        processing_queue.extend(parenttpart)


    return df




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

