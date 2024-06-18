import SQLexecutor as SQLexe
from psycopg2 import sql

############################
## Insert into offchainDB ##
############################

def insert_data(partsid, totalemissions, emissions):
    SQL = sql.SQL("""
            INSERT INTO offchaindb_co2emissions (partsid, totalemissions, emissions) VALUES ({PartsID}, {TotalEMISSIONS}, {EMISSIONS})
            ON CONFLICT (partsid)
            DO UPDATE SET totalemissions = {TotalEMISSIONS}, emissions = {EMISSIONS};
        """).format(
            PartsID = sql.Literal(partsid),
            TotalEMISSIONS = sql.Literal(totalemissions),
            EMISSIONS = sql.Literal(emissions)
        )

    SQLexe.COMMANDexecutor(SQL, 'off')


#######################################
## Get values from offchainDB or WSV ##
#######################################

def get_TotalEMISSIONS(partsid, db = 'off'):
    tablename = 'offchaindb_co2emissions'

    if db == 'wsv':
        tablename = 'co2emissions'

    SQL = sql.SQL("""
            SELECT totalemissions FROM {TABLEname} WHERE partsid = {PartsID};
        """).format(
            TABLEname = sql.Identifier(tablename),
            PartsID = sql.Literal(partsid)
        )

    return SQLexe.QUERYexecutor(SQL, db)[0][0]


def get_EMISSIONS(partsid, db = 'off'):
    tablename = 'offchaindb_co2emissions'

    if db == 'wsv':
        tablename = 'co2emissions'

    SQL = sql.SQL("""
            SELECT emissions FROM {TABLEname} WHERE partsid = {PartsID};
        """).format(
            TABLEname = sql.Identifier(tablename),
            PartsID = sql.Literal(partsid)
        )

    return SQLexe.QUERYexecutor(SQL, db)[0][0]


if __name__ == '__main__':

    partsid = 'e01001'
    totalemissions = 331.01
    emissions = 1.33

    #insert_data(partsid, totalemissions, emissions)

    print(get_TotalEMISSIONS(partsid, 'wsv'))