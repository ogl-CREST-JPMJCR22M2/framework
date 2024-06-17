import common
import sys #コマンドライン変数

def more_quickly_validasion(partsid):
    wsv_value = common.get_TotalEMISSIONS(partsid, 'wsv') # 比較先:WSV上の値
    offdb_value = common.get_TotalEMISSIONS(partsid, 'off') # 比較元:offchainDB上の値

    if wsv_value != offdb_value:
        print("Validation Failed")
    else :
        print("Validation Successful")


def quickly_validasion(partsid):
    offdb_value = common.get_TotalEMISSIONS(partsid, 'off') # 比較元:offchainDB上の値

    """ WSV上の値を用いたchild_totalEmissionの計算 """
    child_partsid = common.get_ChlidParts(partsid) # 下位部品のPartsIDの取得
    sum_child_emissions = 0
    for i in range(len(childpartsid)) :　# child_totalEmissionの取得と合計
        sum_child_emissions += common.get_TotalEMISSIONS(i, 'wsv') 
    
     """ TotalEmissionの再計算 """
    emissions = common.get_TotalEMISSIONS(partsid, 'wsv') # child_totalEmissionの取得と合計
    common.IROHA_COMMANDexecutor(partsid, emissions, sum_child_emissions, 'admin@test') # コマンドによる再計算

    """ データ検証 """
    wsv_value = common.get_TotalEMISSIONS(partsid, 'wsv')
    
    if wsv_value != offdb_value:
        print("Validation Failed")
    else :
        print("Validation Successful")
        

def calculate_totalemissions(partsid):
    childpartsid = common.get_ChlidParts(partsid)
    emissions = common.get_TotalEMISSIONS(partsid, 'wsv')   # child_totalEmissionの取得と合計
    
    if not childpartsid :
        common.IROHA_COMMANDexecutor(partsid, emissions, 0.0, 'admin@test') # コマンドによる再計算
        return common.get_TotalEMISSIONS(partsid, 'wsv')

    else :
        data =  0
        for i in range(len(childpartsid)):
            data += calculate_totalemissions(childpartsid[i])
    
        common.IROHA_COMMANDexecutor(partsid, emissions, data, 'admin@test') # コマンドによる再計算
        return data

    

def original_validatioin(partsid):
    offdb_value = common.get_TotalEMISSIONS(partsid, 'off') # 比較元:offchainDB上の値
    calculate_totalemissions(partsid)

    """ データ検証 """
    wsv_value = common.get_TotalEMISSIONS(partsid, 'wsv')
    
    if wsv_value != offdb_value:
        print("Validation Failed")
    else :
        print("Validation Successful")

if __name__ == '__main__':

    #insert_data(partsid, totalemissions, emissions)

    quickly_calculate_totalemissions('P01001')