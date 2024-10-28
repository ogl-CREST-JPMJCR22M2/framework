#!/bin/bash

export PGPASSWORD=mysecretpassword

datalink=("postgresA" "postgresB" "postgresC")

psql -U postgres -d offchaindb -h ${datalink[0]} -c "\copy offchaindb_cfpval (partsid, totalcfp, cfp) from '/root/dataset/init/A10000.csv' with csv header;"
psql -U postgres -d offchaindb -h ${datalink[1]} -c "\copy offchaindb_cfpval (partsid, totalcfp, cfp) from '/root/dataset/init/B10000.csv' with csv header;"
psql -U postgres -d offchaindb -h ${datalink[2]} -c "\copy offchaindb_cfpval (partsid, totalcfp, cfp) from '/root/dataset/init/C10000.csv' with csv header;"
       

for datalink in ${datalink[@]}; do
    psql -U postgres -d iroha_default -h $datalink -c "\copy cfpval (partsid, totalcfp) from '/root/dataset/cfpval_10000.csv' with csv header;"
    psql -U postgres -d iroha_default -h $datalink -c "\copy partsinfo (partsid, datalink, parents_partsid) from '/root/dataset/init/partsinfo10000.csv' with csv header;"
done

exit $?

results/30000/Acfpval_30000.csv