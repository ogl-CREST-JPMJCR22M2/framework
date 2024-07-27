import commons

def naive_validation(partsid, peer):

    commons.IROHA_COMMANDexecutor(partsid,'SetAccountDetail', peer)


if __name__ == '__main__':

    partsid = 'P01001'
    naive_validation(partsid,'postgresA')