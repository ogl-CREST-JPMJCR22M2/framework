import csv
import random

# ファイル名
filename = 'output.csv'

# データを生成
data = []
data.append(['partsid', 'datalink', 'cfp', 'parents_partsid', 'totalcfp'])

values = ['postgresA', 'postgresB', 'postgresC']
j = 1
for i in range(1, 10001):
    part_id = f'P{i:05d}'  # 'P' + 5桁の連番
    second_value = random.choice(values)  # ランダムに選択
    third_value = round(random.uniform(0.0, 10.0), 3)  # 0.0から10.0の範囲の数値、有効桁数4
    if i == 1:
        second_value = 'postgresA'
        fourth_value = 'NULL'
    else:
        fourth_value = f'P{j:05d}'  # 'P' + 5桁の連番でjを表現
        if (i-1) % 3 == 0:
            j += 1

    if i < 3334:
        fifth_valure = 0.0
    else :
        fifth_valure = third_value

    data.append([part_id, second_value, third_value, fourth_value, fifth_valure])

# CSVファイルに書き込む
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print(f'Data has been written to {filename}')
