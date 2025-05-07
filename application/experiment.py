### 1000回の更新トランザクションのうち，更新対象部品が更新される割合をPareto分布に従って決定

import numpy as np
import matplotlib.pyplot as plt
import random
import polars as pl
from collections import Counter
import time

import update_cfp as u
import write_to_db as w


# Set seed for reproducibility
np.random.seed(42)

num_total_parts = 19531
num_transactions = 1000
update_percent = 1.0 # %で

# ===== 更新対象部品を選ぶ =======
parts = [f"P{i}" for i in range(num_total_parts)]

# ランダムに選択
sampled_parts = random.sample(parts, int(num_total_parts * update_percent * 0.01))
num_part = len(sampled_parts)


# Uniform distribution: each partition has equal probability
uniform_transactions = np.random.randint(0, num_part, num_transactions)

# Pareto distribution: skewed access to partitions
alpha = 1.5
raw_pareto = np.random.pareto(alpha, num_transactions)
pareto_transactions = np.floor(num_part * raw_pareto / (raw_pareto.max() + 1e-8)).astype(int)

# ===== インデックスから部品IDに変換 =====
mapped_parts_u = [sampled_parts[i] for i in uniform_transactions]
mapped_parts_p = [sampled_parts[i] for i in pareto_transactions]

# ===== カウント集計 =====
count_u = Counter(mapped_parts_u)
labels_u, values_u = zip(*count_u.items())

count = Counter(mapped_parts_p)
labels, values = zip(*count.items())


# Create histograms for visualization
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.bar(labels_u, values_u, edgecolor='black')
plt.title('Uniform Distribution of Transactions')
plt.xlabel('Partid')
plt.ylabel('Frequency')

# ===== 棒グラフ描画 =====
plt.subplot(1, 2, 2)
plt.bar(labels, values, edgecolor='black')
plt.xticks(rotation=90)
plt.title('Pareto Distribution of Transactions (alpha=1.5)')
plt.xlabel('Partid')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()
"""

# Prepare the data for display
df = pl.DataFrame({
    'Transaction_ID': range(1, num_transactions + 1),
    'Uniform_Partition': mapped_parts_u,
    'Pareto_Partition': mapped_parts_p
})

print(df)


start = time.time()

for i in mapped_parts_u:

    assembler = w.get_Assebler(i)
    u.update_hash(assembler, i, random.random())

t = time.time() - start

print("total time:", t)
print("average time:", t/num_transactions)"""