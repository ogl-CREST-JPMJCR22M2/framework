### partidを使って求める

from sqlalchemy import create_engine
import polars as pl
from psycopg2 import connect, sql
from psycopg2.extras import execute_values
import SQLexecutor as SQLexe



### irohaに渡すためのデータ加工 rm

def to_iroha(df):

    part_list = df["partid"].to_list()
    hash_list = df["hash"].to_list()

    return part_list, hash_list


### offchaindbのcfpの更新

def update_co2_to_off(assembler, target_part, co2 = None, cfp = None, sabun = None):

    if cfp == None and co2 == None and sabun != None :

        sql_statement = sql.SQL(
            """
            UPDATE cfpval SET cfp = cfp - {sabun} WHERE partid = {target_part};
            """
        ).format(
            target_part = sql.Literal(target_part),
            sabun = sql.Literal(sabun)
        )
        SQLexe.COMMANDexecutor_off(sql_statement, assembler)

    elif cfp == None and co2 != None and sabun != None :

        sql_statement = sql.SQL(
            """
            UPDATE cfpval set (cfp, co2) = (cfp - {sabun}, {co2}) where partid = {target_part};
            """
        ).format(
            target_part = sql.Literal(target_part),
            sabun = sql.Literal(sabun),
            co2 = sql.Literal(co2)
        )

        SQLexe.COMMANDexecutor_off(sql_statement, assembler)
    
    elif cfp != None and co2 == None and sabun == None :

        sql_statement = sql.SQL(
            """
            UPDATE cfpval set cfp = {cfp} where partid = {target_part};
            """
        ).format(
            target_part = sql.Literal(target_part),
            cfp = sql.Literal(cfp)
        )

        SQLexe.COMMANDexecutor_off(sql_statement, assembler)


### ASSEMBLERを取得

def get_Assebler(target_part):

    sql_statement = sql.SQL(
            """
            SELECT * FROM partinfo WHERE partid = {target_part};
            """
        ).format(
            target_part = sql.Literal(target_part)
        )
        
    return SQLexe.QUERYexecutor_on(sql_statement, "postgresA")[0][1]


### ハッシュ値を取得

def get_hash(target_part):

    sql_statement = sql.SQL(
            """
            SELECT hash FROM hash_parts_tree WHERE partid = {target_part};
            """
        ).format(
            target_part = sql.Literal(target_part)
        )
        
    return SQLexe.QUERYexecutor_on(sql_statement, "postgresA")[0][1]


