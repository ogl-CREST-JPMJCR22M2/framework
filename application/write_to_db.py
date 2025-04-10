


def store_in_postgresql(df, peer):
    
    engine = create_engine("postgresql://postgres:mysecretpassword@postgres"+peer+":5432/offchaindb")
    common_sql_state = "SQLSTATE: 42P07"
    
    try:
        df.write_database(table_name, connection=uri,
                          engine='adbc', if_exists='replace')
        print('loading has been completed!')
    except Exception as e:
        if(common_sql_state in str(e)):
            df.write_database(table_name, connection=uri,
                          engine='adbc', if_exists='append')
            print('loading has been completed!')
        else:
            print(e)