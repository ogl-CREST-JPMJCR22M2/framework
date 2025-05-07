### 1000回の更新トランザクションのうち，更新対象部品が更新される割合をPareto分布に従って決定

import numpy as np
import matplotlib.pyplot as plt
import random
import polars as pl
import time
from psycopg2 import sql
from sqlalchemy import create_engine

import calculation as c
import write_to_db as w
import varification_2 as v2
import SQLexecutor as SQLexe

# ===== リセット =======
#c.make_merkltree("postgresA", "P0", True)

# Set seed for reproducibility
np.random.seed(42)

num_total_parts = 19531
num_transactions = 1000
update_percent =  10.0 # %で

# ===== 更新対象部品を選ぶ =======
parts = [f"P{i}" for i in range(num_total_parts)]

# ランダムに選択
per = random.sample(parts, int(num_total_parts * update_percent * 0.01))

df_va = pl.DataFrame({
    "partid":per
})


# ======== 部品木の取得 ======== #

def get_part_tree(peer, parents_partid):

    engine = create_engine("postgresql://postgres:mysecretpassword@"+peer+":5432/iroha_default")

    sql_statement ="SELECT r.partid, assembler FROM partrelationship r, partinfo i WHERE r.partid = i.partid;"

    all_tree = pl.read_database(sql_statement, engine)
    
    return all_tree


df = get_part_tree("postgresA", "P0")

df = df.join(df_va, on="partid", how="inner")


df_B = df.filter(pl.col("assembler") == "postgresB")
df_C = df.filter(pl.col("assembler") == "postgresC")

Blist = df_B["partid"].to_list()
Clist = df_C["partid"].to_list()

def upsert_exe(lists, assembler):

    sql_statement = sql.SQL(
        """
        UPDATE cfpval SET cfp = '10000.0' WHERE partid IN ({part_ids});
        """
    ).format(
        part_ids = sql.SQL(', ').join(map(sql.Literal, lists))
        )
    SQLexe.COMMANDexecutor_off(sql_statement, assembler)

upsert_exe(Blist, "postgresB")
upsert_exe(Clist, "postgresC")


#=====================================================


# ===== 更新対象部品を選ぶ =======
parts = [f"P{i}" for i in range(num_total_parts)]

# ランダムに選択
sampled_parts = random.sample(parts, num_total_parts)

# Uniform distribution: each partition has equal probability
uniform_transactions = np.random.randint(0, num_total_parts, num_transactions)

# Pareto distribution: skewed access to partitions
alpha = 1.5
raw_pareto = np.random.pareto(alpha, num_transactions)
pareto_transactions = np.floor(num_total_parts * raw_pareto / (raw_pareto.max() + 1e-8)).astype(int)

# ===== インデックスから部品IDに変換 =====
mapped_parts_u = [sampled_parts[i] for i in uniform_transactions]
mapped_parts_p = [sampled_parts[i] for i in pareto_transactions]

r = set()

start = time.time()

for i in mapped_parts_p:

    # print(i)

    assembler = w.get_Assebler(i)
    result = v2.make_merkltree_varification(assembler, i)
    #print(r)

    if result != None:
        r = r | set(v2.make_merkltree_varification(assembler, i))

t = time.time() - start

print("total time:", t)
print("average time:", t/num_transactions)
#print("Specific failure:", set(per)-r)
print("Specific rate:", len(r)/len(per)*100) 
