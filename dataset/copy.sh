#!/bin/bash

export PGPASSWORD=mysecrestpassword

dabalink=("postgresA" "postgresB" "postgresC")

for dabalink in ${dabalink[@]}; do

    if [ $datalink -eq "postgresA"]; then
        psql -U postgres -d offchaindb -h $dabalink -c "\copy offchaindb_cfpval (partsid, totalcfp, cfp) from '/root/dataset/A10000.csv' with csv header;"
    elif [ $datalink -eq "postgresB"]; then
        psql -U postgres -d offchaindb -h $dabalink -c "\copy offchaindb_cfpval (partsid, totalcfp, cfp) from '/root/dataset/B10000.csv' with csv header;"
    else
        psql -U postgres -d offchaindb -h $dabalink -c "\copy offchaindb_cfpval (partsid, totalcfp, cfp) from '/root/dataset/C10000.csv' with csv header;"
    fi

    psql -U postgres -d iroha_default -h $dabalink -c "\copy cfpval (partsid, totalcfp) from '/root/dataset/data_10000_cfpval.csv' with csv header;"
    psql -U postgres -d iroha_default -h $dabalink -c "\copy partsinfo (partsid, datalink, parents_partsid) from '/root/dataset/data_10000_info.csv' with csv header;"
done

exit $?