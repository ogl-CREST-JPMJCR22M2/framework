### partidを使って求める

from sqlalchemy import create_engine, text
import polars as pl
import time
import hashlib
from decimal import *
import zlib

import SQLexecutor as SQLexe
import write_to_db as w


# ======== DataFrameの表示の仕方 ======== #
pl.Config.set_tbl_cols(-1)
pl.Config.set_tbl_rows(-1)
pl.Config.set_fmt_str_lengths(n=30)
# ===================================== #


# ======== 部品木の取得 ======== #

def get_part_tree(peer, peers, root_partid):

    engine = create_engine("postgresql://postgres:mysecretpassword@"+peer+":5432/iroha_default")

     # offchain-dbからcfpの算出
    sql_import = " UNION ALL ".join( 
            ["SELECT * FROM dblink('host="+ p +" port=5432 dbname=offchaindb user=postgres password=mysecretpassword', 'SELECT partid, co2 FROM cfpval') AS t1(partid CHARACTER varying(288), co2 DECIMAL)"
            for p in peers ])

    sql_ =  "WITH plain_cfp AS (" + sql_import + "),"

    # 部品木の抽出
    sql_ =  sql_ + """
            part_tree AS( 
                WITH RECURSIVE calc(partid, parents_partid, priority) AS 
                    ( 
                        SELECT partid, parents_partid, priority
                        FROM partrelationship r
                        WHERE partid =  """ + "'"+ root_partid + "'"+ """

                        UNION ALL 

                        SELECT r.partid, r.parents_partid, r.priority
                        FROM partrelationship r, calc 
                        WHERE r.parents_partid = calc.partid 
                    ) 
                    SELECT calc.partid, parents_partid, priority, co2 
                    FROM  calc, plain_cfp
                    WHERE calc.partid = plain_cfp.partid
                ), """

    # totalcfpの算出        
    sql_ =  sql_ + """
        get_totalcfp AS (
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
        SELECT pt.partid, parents_partid, priority, assembler, cfp, co2
        FROM part_tree pt, get_totalcfp gt, partinfo i
        WHERE pt.partid = gt.partid AND pt.partid = i.partid;
        """
   

    df = pl.read_database(text(sql_), engine)

    return df

# ======== 算出部分 ======== #

# ハッシュ化    
def sha256(value: float) -> str:
    return hashlib.sha256(str(value).encode()).hexdigest()
  
def crc32(value: float) -> str:
    return format(zlib.crc32(str(value).encode()) & 0xFFFFFFFF, '08x')

# Decimal
def to_dechimal(value: float) -> Decimal:
    return Decimal(value).quantize(Decimal('0.0001'), ROUND_HALF_UP)

# ハッシュ値を計算する関数
def compute_parent_hashes(df):

    # 末端ノードのハッシュ値を決定
    df = df.with_columns(
        pl.when(~pl.col("partid").is_in(df["parents_partid"]))
        .then(pl.col("co2").map_elements(sha256, return_dtype=pl.String))
        .otherwise(None)
        .alias("hash")
    )

    # 子ノードリストを作成
    child_list = df.select(["partid", "parents_partid"]).group_by("parents_partid").agg(pl.col("partid").alias("child_parts")).rename({"parents_partid": "partid"})
    
    df = df.join(child_list, on="partid", how="left")
        
        
    # 子部品のハッシュの連結
    def get_child_hashes(parts: list[str]) -> str:

        df_ =  df.filter(pl.col("partid").is_in(parts))
        df_ = df_.sort(["priority"])

        hash_values = df_["hash"].to_list()

        clean_hashes = []

        for h in hash_values:
            if h is None:
                return None
            else:
                clean_hashes.append(h)
        
        out = "".join(clean_hashes)
        
        return out

    # ハッシュ値を計算
    while df["hash"].null_count() > 0:

        df = df.with_columns(
            pl.when((pl.col("hash").is_null()) & (pl.col("child_parts").is_not_null()))
            .then(
                pl.concat_str([
                    pl.col("co2").map_elements(sha256, return_dtype=pl.String),
                    pl.col("child_parts").map_elements(get_child_hashes, return_dtype=pl.String)
                    ])
                    .map_elements(crc32, return_dtype=pl.String)
            )
            .otherwise(pl.col("hash"))
            .alias("hash")
        )

    return df



def make_merkltree(assembler, root_partid, write_totalcfp = False):

    peers = ["postgresA", "postgresB", "postgresC"]

    df = get_part_tree(assembler, peers, root_partid) # root_partidがルートの部品木の抽出 

    result = compute_parent_hashes(df) # マークル木を計算

    # Irohaコマンドで書き込み
    part_list, hash_list = w.to_iroha(result)

    SQLexe.IROHA_CMDexe(assembler, part_list, hash_list)
    
    # 各offchainに書き込み
    if write_totalcfp == True:

        result_a = result['partid', 'assembler', 'cfp'] #必要な列だけ抽出

        assembler_list = result_a.unique(subset=['assembler'])['assembler'].to_list()

        for a in assembler_list:

            df_a = result_a.filter(pl.col("assembler") == a)
            w.upsert_totalcfp_exe(df_a, a)
        
    return result



# ======== MAIN ======== #

if __name__ == '__main__':

    root_partid = 'P0'
    assembler = w.get_Assebler(root_partid)

    start = time.time()

    df = make_merkltree(assembler, root_partid, True)
    
    t = time.time() - start
    print("time:", t)


