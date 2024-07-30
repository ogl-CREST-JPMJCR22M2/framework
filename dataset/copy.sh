#!/bin/bash

export PGPASSWORD=mysecretpassword

datalink=("postgresA" "postgresB" "postgresC")

for datalink in ${datalink[@]}; do

    if [ $datalink -eq "postgresA"]; then
        psql -U postgres -d offchaindb -h $datalink -c "\copy offchaindb_cfpval (partsid, totalcfp, cfp) from '/root/dataset/A10000.csv' with csv header;"
    elif [ $datalink -eq "postgresB"]; then
        psql -U postgres -d offchaindb -h $datalink -c "\copy offchaindb_cfpval (partsid, totalcfp, cfp) from '/root/dataset/B10000.csv' with csv header;"
    else
        psql -U postgres -d offchaindb -h $datalink -c "\copy offchaindb_cfpval (partsid, totalcfp, cfp) from '/root/dataset/C10000.csv' with csv header;"
    fi

    psql -U postgres -d iroha_default -h $datalink -c "\copy cfpval (partsid, totalcfp) from '/root/dataset/data_10000_cfpval.csv' with csv header;"
    psql -U postgres -d iroha_default -h $datalink -c "\copy partsinfo (partsid, datalink, parents_partsid) from '/root/dataset/data_10000_info.csv' with csv header;"
done

exit $?