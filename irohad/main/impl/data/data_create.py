import pandas as pd

# データ読み込み（CSVファイルのパスを指定）
df = pd.read_csv("/root/framework_/irohad/main/impl/data/partsinfo.csv")

# SQL INSERT文のテンプレート
table_name = "partsinfo"
columns = ", ".join(df.columns)
sql_insert_statements = []

# 各行に対してINSERT文を生成
sql_insert_statements.append(f"INSERT INTO {table_name} ({columns}) VALUES ")
for index, row in df.iterrows():
    values = ", ".join([f"'{str(value)}'" for value in row])
    if index != 29999:
        sql_insert_statements.append(f"({values}),")
    else:
        sql_insert_statements.append(f"({values});")

# 結果を表示またはファイルに書き出し
with open("/root/framework_/irohad/main/impl/data/insert_partsinfo.sql", "w") as file:
    file.write("\n".join(sql_insert_statements))