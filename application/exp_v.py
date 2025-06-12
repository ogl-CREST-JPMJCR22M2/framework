### 1000回の更新トランザクションのうち，更新対象部品が更新される割合をPareto分布に従って決定

import numpy as np
import random
import polars as pl
import time
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import create_engine
from psycopg2 import connect, sql
from psycopg2.extras import execute_values

import SQLexecutor as SQLexe
import write_to_db as w
import varification as v
import calculation as c

# Set seed for reproducibility
np.random.seed(42)

num_total_parts = 19531
num_transactions = 1000
kaizan_percent = [1.0, 5.0, 10.0, 15.0, 20.0] # %で
percent = kaizan_percent[4]

#init
root_partid = 'P0'
peers = ["postgresA", "postgresB", "postgresC"]
assembler = w.get_Assebler(root_partid)
c.make_merkltree(assembler, root_partid)

# kaizan part select 
parts = [f"P{i}" for i in range(num_total_parts)]

per = random.sample(parts, int(num_total_parts * percent * 0.01))

df_va = pl.DataFrame({
    "partid":per,
    "cfp": random.random()
})

engine = create_engine("postgresql://postgres:mysecretpassword@postgresA:5432/iroha_default")
sql_statement ="SELECT partid, assembler FROM partinfo;"
df = pl.read_database(sql_statement, engine)

df = df.join(df_va, on="partid", how="inner")


df_B = df.filter(pl.col("assembler") == "postgresB")
df_C = df.filter(pl.col("assembler") == "postgresC")

Blist = df_B.select(["partid", "cfp"]).rows()
Clist = df_C.select(["partid", "cfp"]).rows()

# offchain-dbへの書き込み
def kaizan(peer, lists):

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
        host = peer,
        port = 5432
    )

    with conn.cursor() as cur:
        execute_values(cur, upsert_sql, lists)

    conn.commit()
    conn.close()

kaizan("postgresB", Blist)
kaizan("postgresC", Clist)

start = time.time()
result = v.valification(assembler, peers, root_partid)
t = time.time() - start

print("time:", t)

#rset = set(rlist)
#print("Specific num:", len(result))
#print("Kaizan num:", len(per))
print("Specific rate:", len(result)/len(per)*100)
#print(set(result)-set(per))
#print(set(result))
#print(set(per))


"""
# ===== 更新対象部品を選ぶ =======
parts = [f"P{i}" for i in range(num_total_parts)]
sampled_parts = random.sample(parts, num_total_parts)

# Pareto distribution: skewed access to partitions
alpha = 1.5
raw_pareto = np.random.pareto(alpha, num_transactions)
pareto_transactions = np.floor(num_total_parts * raw_pareto / (raw_pareto.max() + 1e-8)).astype(int)

# ===== インデックスから部品IDに変換 =====
mapped_parts_p = [sampled_parts[i] for i in pareto_transactions]

# ===== トランザクション実行関数 =====
def exec_transaction(target_part):

    assembler = w.get_Assebler(target_part)
    result = v.valification(assembler, peers, target_part)
    return result

# ===== 実行 ====

#rlist = []

total_start = time.time()

with ThreadPoolExecutor(max_workers=10) as executor:
    r = executor.map(exec_transaction, mapped_parts_p)

total_elapsed = time.time() - total_start

print("total time: ", total_elapsed)
print("average time:", total_elapsed / num_transactions)

#エラー回避のためのlist->tuple
rlist = list(r)
rlist_ = []

for i in rlist:
    if len(i) != 0:
        rlist_.append(i[0])

rset = set(rlist_)
print("Specific num:", len(rset))
print("Kaizan num:", len(per))
print("Specific rate:", len(rset)/len(per)*100)
"""