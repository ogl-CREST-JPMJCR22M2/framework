### cfpが変更された時にtarget_partがパスに含まれる全ての部品のhashを更新する
### cfpが変更された時にtotalcfpを更新する

from sqlalchemy import create_engine
import polars as pl
from psycopg2 import sql
import hashlib
import calculation as cal
import SQLexecutor as SQLexe
from decimal import *
import write_to_db as w

### パス（変更対象部品）の取得

def get_path(target_part, peer):

    engine = create_engine("postgresql://postgres:mysecretpassword@postgres"+peer+":5432/iroha_default")
    sql_statement ="SELECT partid, parents_partid FROM partrelationship;"

    all_tree = pl.read_database(sql_statement, engine) #木の全体

    parents_partid = all_tree.filter(pl.col("partid") == target_part)["parents_partid"]
    parents_list = [target_part]

    while parents_partid.item() != 'null':

        parents_list.append(parents_partid.item())
        
        parents_partid = all_tree.filter(pl.col("partid") == parents_partid)["parents_partid"]

    sql_info ="SELECT partid, assembler FROM partinfo;"
    tree_info = pl.read_database(sql_info, engine)

    target_tree = tree_info.filter(pl.col("partid").is_in(parents_list))
    
    return parents_list, target_tree


###  ハッシュの更新

def update_hash(target_part, new_cfp):

    # パスを取得
    path, tree = get_path(target_part, "A")

    # == cfpの差分を計算 == #
    new_cfp =  Decimal(new_cfp).quantize(Decimal('0.0001'), ROUND_HALF_UP) # new_cfpの小数点以下4桁まで表示

    assembler = tree.filter(pl.col("partid") == target_part)["assembler"].item() # assemblerの取得

    sql_statement = sql.SQL("SELECT cfp FROM cfpval where partid = {target_part};" # 既存のCFPを取得
    ).format(
            target_part = sql.Literal(target_part)
    )
    pre_cfp = SQLexe.QUERYexecutor_off(sql_statement, assembler)[0][0]

    cfp_sabun = new_cfp - pre_cfp #差分を計算

    # == 順番に処理する == #

    while len(path) > 0:

        target_part = path.pop(0)
        
        assembler = tree.filter(pl.col("partid") == target_part)["assembler"].item() # assemblerを取得

        w.update_cfp_to_off(assembler, target_part, new_cfp, cfp_sabun) # 新しいtotalCFPを書き込み

        new_cfp = None # 一回目だけnew_cfpを更新するため
    

update_hash("P1", 0.1)