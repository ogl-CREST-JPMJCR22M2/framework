### cfpが変更された時にtarget_partがパスに含まれる全ての部品のhashを更新する
### cfpが変更された時にtotalcfpを更新する

from sqlalchemy import create_engine
import polars as pl
from psycopg2 import sql
import hashlib
from decimal import *
import time

import calculation as c
import SQLexecutor as SQLexe
import write_to_db as w


# ======== DataFrameの表示の仕方 ======== #
pl.Config.set_tbl_cols(-1)
pl.Config.set_tbl_rows(-1)
pl.Config.set_fmt_str_lengths(n=64)
# ===================================== #



# ====== パス（変更対象部品）の取得 ====== #

def get_path(assembler, target_part):

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

            ## 差分の算出
            sql_ = f"SELECT "

            ## 一時テーブルの構築
            cur.execute("""
                CREATE TEMP TABLE temp (
                    partid CHARACTER varying(288),
                    parents_partid CHARACTER varying(288),
                    assembler CHARACTER varying(288),
                    cfp DECIMAL, 
                    co2 DECIMAL,
                    hash CHARACTER varying(64),
                    PRIMARY KEY (partid)
                );

                CREATE TEMP TABLE temp_tree (
                    partid CHARACTER varying(288)
                    PRIMARY KEY (partid)
                );
            """)

            ## cfpの算出
            # offchain-dbからcfpの算出
            cfp_import = " UNION ALL \n".join(["SELECT * FROM dblink('host="+ p +" port=5432 dbname=offchaindb user=postgres password=mysecretpassword', 'SELECT partid, co2 FROM cfpval') AS t1(partid CHARACTER varying(288), co2 DECIMAL)" 
            for p in peers ]) 
        
            sql_ = f"""
                INSERT INTO temp_tree (partid)
                WITH RECURSIVE path(partid, parents_partid, assembler) AS
                (
                    SELECT partid, parents_partid
                    FROM partrelationship r
                    WHERE partid = 'P30'

                    UNION ALL 

                    SELECT r.partid, r.parents_partid
                    FROM partrelationship r, path 
                    WHERE r.partid = path.parents_partid 
                )
                SELECT * FROM path;

                INSERT INTO temp (partid, parents_partid, assembler, cfp, co2, hash) 
                SELECT tt.partid, tt.parents_partid, assembler, 0, 0, 
                        CASE 
                            WHEN tt.partid IS NOT NULL THEN 'null'
                            ELSE mt.hash
                        END AS hash
                FROM temp_tree tt, partinfo pi, hash_parts_tree mt
                WHERE pi.parents_partid = tt.partid AND pi.parents_partid = mt.partid OR pi.partid = 'P0';




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
                        FROM  calc, plain_cfp
                        WHERE calc.partid = plain_cfp.partid
                ), 
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
                SELECT pt.partid, parents_partid, priority, assembler, cfp, co2, 'null'
                FROM part_tree pt, get_totalcfp gt, partinfo i
                WHERE pt.partid = gt.partid AND pt.partid = i.partid;

                UPDATE temp SET hash = encode(digest(cfp::TEXT, 'sha256'), 'hex')
                    WHERE NOT EXISTS (SELECT parents_partid FROM partrelationship WHERE partrelationship.parents_partid = temp.partid);

                SELECT * FROM temp WHERE hash = 'null'
            """
            cur.execute(sql_, (root_partid,))
            
            not_hashed = cur.fetchall()

            while len(not_hashed) > 0: 

                sql_2 = """ 
                    WITH can_hashing AS (
                        SELECT parents_partid, bool_and(hash != 'null') as result FROM temp
                        Group by parents_partid
                    )
                    SELECT temp.parents_partid, array_agg(hash)
                    FROM can_hashing, temp
                    WHERE result = True AND can_hashing.parents_partid = temp.parents_partid
                    Group by temp.parents_partid;
                """ 
                cur.execute(sql_2)
                queue = cur.fetchall()

                for q in queue:
                    xor_hashed = xor_hash(q[1])

                    sql_32 = f"UPDATE temp SET hash = encode(digest( encode(digest(cfp::TEXT, 'sha256'), 'hex')||'{xor_hashed}' ::TEXT, 'sha256'), 'hex') WHERE partid = %s"
                    cur.execute(sql_32,  (q[0],))
                
                # 終了条件のアップデート
                sql_4 = "SELECT * FROM temp WHERE hash = 'null';"
                cur.execute(sql_4)
                not_hashed = cur.fetchall()

            sql_5 = "SELECT partid, assembler, cfp, hash as hashval FROM temp;"
            cur.execute(sql_5)
            data = cur.fetchall()

    finally:
        if conn:
            conn.close()
    
    return data

    engine = create_engine("postgresql://postgres:mysecretpassword@"+assembler+":5432/iroha_default")
    #sql_statement ="""
    #    SELECT r.partid, parents_partid, priority, assembler, hash \
    #        FROM partrelationship r, partinfo i, hash_parts_tree m \
    #        WHERE r.partid = i.partid and r.partid = m.partid;
    #"""

    sql_statement = """
        WITH part_tree AS(
            WITH RECURSIVE calc(partid, parents_partid) AS
                (
                    SELECT partid, parents_partid, priority
                    FROM partrelationship r
                    WHERE partid = 'P0'
                    UNION ALL
                    SELECT r.partid, r.parents_partid, r.priority
                    FROM partrelationship r, calc
                    WHERE r.parents_partid = calc.partid 
                )
                SELECT *
                FROM calc
        )
        SELECT c.partid, parents_partid, priority, assembler, hash
        FROM part_tree c, partinfo i, hash_parts_tree m
        WHERE c.partid = i.partid and c.partid = m.partid;
            
    """

    all_tree = pl.read_database(sql_statement, engine) #木の全体

    parents_partid = all_tree.filter(pl.col("partid") == target_part)["parents_partid"]
    parents_list = [target_part]

    while len(parents_partid) >  0:

        parents_list.append(parents_partid.item())

        if parents_partid.item() == 'null': break # 終了条件
        
        parents_partid = all_tree.filter(pl.col("partid") == parents_partid)["parents_partid"]

    target_tree = all_tree.filter(pl.col("parents_partid").is_in(parents_list)) # 必要なとこだけ抽出

    return parents_list, target_tree



# ====== ハッシュの再計算 ====== #

def recalcu_hash(df, partid):

    child_df = df.filter((pl.col("parents_partid") == partid)).sort(["priority"])
    child_hash_list = child_df.get_column("hash").to_list()

    target_cfp_hash = df.filter(pl.col("partid") == partid)["hash"].item() # 更新するpartidのhashを取得

    new_hash = c.sha256(target_cfp_hash + "".join(child_hash_list)) # 新しいハッシュ

    return new_hash
    
    

# ====== パスのハッシュとtotalcfpを計算 ====== #

def update_hash(assembler, target_part, new_cfp):

    # パスとツリーを取得
    path, tree = get_path(assembler, target_part)

    ## cfpの差分を計算
    new_cfp =  Decimal(new_cfp).quantize(Decimal('0.0001'), ROUND_HALF_UP) # new_cfpの小数点以下4桁まで表示

    sql_statement = sql.SQL("SELECT co2 FROM cfpval where partid = {target_part};" # 既存のCFPを取得
    ).format(
            target_part = sql.Literal(target_part)
    )

    pre_cfp = SQLexe.QUERYexecutor_off(sql_statement, assembler)[0][0]

    cfp_sabun = pre_cfp - new_cfp #差分を計算

    ## hash(new_cfp)を書き込み 

    new_hash = c.sha256(new_cfp)
    tree = tree.with_columns(
        pl.when(pl.col("partid") == target_part)
        .then(pl.lit(c.sha256(new_cfp)))
        .otherwise(pl.col("hash"))
        .alias("hash")
    )


    ## 順番に処理する
    cfp = None

    for i in range(len(path)-1):

        target_part = path[i]
        
        assembler_path = w.get_Assebler(target_part) # assemblerを取得
        #print(assembler_path, target_part, new_cfp, cfp, cfp_sabun)
        w.update_co2_to_off(assembler_path, target_part, new_cfp, cfp, cfp_sabun) # 新しいtotalCFPを書き込み

        new_hash = recalcu_hash(tree, target_part)

        # new_hashでdataframeをupdate
        tree = tree.with_columns(
            pl.when(pl.col("partid") == target_part)
            .then(pl.lit(new_hash))
            .otherwise(pl.col("hash"))
            .alias("hash")
        )

        new_cfp = None # 一回目だけnew_cfpを更新するため

    result = tree.filter(pl.col("partid").is_in(path))["partid", "hash"]

    # irohaが完成するまで w.upsert_hash_exe(result, "A")

    # Irohaコマンドで書き込み
    part_list, hash_list = w.to_iroha(result)
    SQLexe.IROHA_CMDexe(assembler, part_list, hash_list)

    return 
    


# ======== MAIN ======== #

if __name__ == '__main__':

    target_part = "P5"
    assembler = w.get_Assebler(target_part)

    start = time.time()

    update_hash(assembler, target_part, 0.50)
    
    t = time.time() - start
    print("time:", t)

    