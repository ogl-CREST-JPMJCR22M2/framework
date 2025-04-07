import SQLexecutor as SQLexe
from psycopg2 import sql
from sqlalchemy import create_engine
import commons as com
import polars as pl
import time
import random
import hashlib

pl.Config.set_tbl_cols(-1)
pl.Config.set_tbl_rows(-1)
pl.Config.set_fmt_str_lengths(n=264)

# offchainに接続，cfpをget
def get_cfpval(peer):

    engine = create_engine("postgresql://postgres:mysecretpassword@postgres"+peer+":5432/offchaindb")

    sql_statement =" SELECT partid, cfp FROM cfpval;"

    df = pl.read_database(sql_statement, engine)
    
    return df


# offchainから全てのcfpをget，結合
def join_cfpvals(peers):

    df1 = get_cfpval(peers[0])

    for p in peers[1:]:
        df2 = get_cfpval(p)
        df1 = pl.concat([df1, df2])

    return df1.with_columns(pl.col("cfp").cast(pl.String).alias("cfp"))


# 部品木全体を取得
def get_tree(peer, parents_partid):

    engine = create_engine("postgresql://postgres:mysecretpassword@postgres"+peer+":5432/iroha_default")

    sql_statement ="SELECT partid, parents_partid FROM partrelationship;"

    all_tree = pl.read_database(sql_statement, engine)

    # 部品木を抽出
    def get_childpart(df, parents_partid):

        child_df = df.filter(pl.col("parents_partid") == parents_partid)

        childpart = child_df["partid"].to_list()

        for child in childpart:
            child_df = pl.concat([child_df, get_childpart(df, child)])
        
        return child_df

    df = pl.concat([all_tree.filter(pl.col("parents_partid").is_in(["null"])), get_childpart(all_tree, parents_partid)])
    
    return df


# ハッシュ化    
def sha256(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()

# ハッシュ値を計算する関数
def compute_parent_hashes(df):

    # 末端ノードのハッシュ値を決定
    df = df.with_columns(
        pl.when(~pl.col("partid").is_in(df["parents_partid"]))
        .then(pl.col("cfp").map_elements(sha256, return_dtype=pl.String))
        #.then(pl.col("cfpval")) #確認用
        .otherwise(None)
        .alias("hash_value")
    )

    # 子ノードリストを作成
    child_hashes = df.select(["partid", "parents_partid"]).group_by("parents_partid").agg(pl.col("partid").alias("child_parts")).rename({"parents_partid": "partid"})
    
    df = df.join(child_hashes, on="partid", how="left")
    
    def get_child_hashes(parts: list[str]) -> str:
        hash_values = df.filter(pl.col("partid").is_in(parts))["hash_value"].to_list()
        clean_hashes = []

        for h in hash_values:
            if h is None:
                return None
            else:
                clean_hashes.append(h)
        
        out = "".join(clean_hashes)
        
        return out

    # ハッシュ値を計算
    while df["hash_value"].null_count() > 0:

        df = df.with_columns(
            pl.when((pl.col("hash_value").is_null()) & (pl.col("child_parts").is_not_null()))
            .then(
                pl.concat_str([
                    pl.col("cfp").map_elements(sha256, return_dtype=pl.String),
                    pl.lit("("),
                    pl.col("child_parts").map_elements(get_child_hashes, return_dtype=pl.String),
                    pl.lit(")"),
                    ]).map_elements(sha256, return_dtype=pl.String)
            )
            .otherwise(pl.col("hash_value"))
            .alias("hash_value")
        )
    
    print(df.drop("child_parts"))    
            
    return df


if __name__ == '__main__':

    peer = "A"
    peers = ["A", "B", "C"]
    partid = 'P0'
    start = time.time()

    df = get_tree(peer, partid)

    """df_h = pl.DataFrame(
        {
            "partid" : ["P"+str(i) for i in range(0, 156)],
            "cfpval" : [str(round(random.random(), 4)) for i in range(0, 156)]
        }
    )
    """

    df_h=join_cfpvals(peers)
    df = df.join(df_h, on=["partid"], how="left")
    
    compute_parent_hashes(df)

    t = time.time() - start
    
    print(t)
    

### ============================================================================================== ###

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

