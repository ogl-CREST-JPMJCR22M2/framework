#!/bin/bash

export PGPASSWORD=mysecretpassword

datalink=("postgresA" "postgresB" "postgresC")

for datalink in ${datalink[@]}; do
    psql -U postgres -d offchaindb -h $datalink -c "delete from offchaindb_cfpval;"
    psql -U postgres -d iroha_default -h $datalink -c "delete from cfpval;"
    psql -U postgres -d iroha_default -h $datalink -c "delete from partsinfo;"
done

exit $?