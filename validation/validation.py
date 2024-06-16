import common
#import SQL
import sys #コマンドライン変数

def more_quickly_validasion(partsid):
    wsv_value = SQL.get_TotalEMISSIONS(partsid, 'wsv') # 比較先:WSV上の値
    offdb_value = SQL.get_TotalEMISSIONS(partsid, 'off') # 比較元:offchainDB上の値

    if wsv_value != offdb_value:
        print("Validation Failed")
    else :
        print("Validation Successful")


def quickly_validasion(partsid):
    offdb_value = SQL.get_TotalEMISSIONS(partsid, 'off') # 比較元:offchainDB上の値

    """ WSV上の値を用いたchild_totalEmissionの計算 """
    child_partsid = common.get_childparts(partsid) # 下位部品のPartsIDの取得
    sum_child_emissions = 0
    for i in range(len(childpartsid)) :　# child_totalEmissionの取得と合計
        sum_child_emissions += SQL.get_TotalEMISSIONS(i, 'wsv') 
    
     """ TotalEmissionの再計算 """
    emissions = SQL.get_TotalEMISSIONS(partsid, 'wsv') # child_totalEmissionの取得と合計
    IROHA_COMMANDexecutor(partsid, emissions, sum_child_emissions, 'admin@test') # コマンドによる再計算

    """ データ検証 """
    wsv_value = SQL.get_TotalEMISSIONS(partsid, 'wsv')
    
    if wsv_value != offdb_value:
        print("Validation Failed")
    else :
        print("Validation Successful")
        

def calculate_totalemissions(partsid):

    if partsid == 'Nan':
         """ TotalEmissionの再計算 """
        emissions = SQL.get_TotalEMISSIONS(partsid, 'wsv') # child_totalEmissionの取得と合計
        return IROHA_COMMANDexecutor(partsid, emissions, sum_child_emissions, 'admin@test') # コマンドによる再計算
    else :
        for i in range(len(childpartsid)) :　# child_totalEmissionの取得と合計
            sum_child_emissions += SQL.get_TotalEMISSIONS(i, 'wsv') 
            calculate_totalemissions(childpartsid[i])
    


def original_validatioin(partsid):
    offdb_value = SQL.get_TotalEMISSIONS(partsid, 'off') # 比較元:offchainDB上の値

    """ child_totalEmissionの計算 """
    child_partsid = common.get_childparts(partsid) # 下位部品のPartsIDの取得
    sum_child_emissions = 0

    calculate_totalemissions(partsid)

    """ データ検証 """
    wsv_value = SQL.get_TotalEMISSIONS(partsid, 'wsv')
    
    if wsv_value != offdb_value:
        print("Validation Failed")
    else :
        print("Validation Successful")

