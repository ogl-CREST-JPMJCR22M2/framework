#!/bin/bash

export PGPASSWORD=mysecretpassword

datalink=("postgresA" "postgresB" "postgresC")

for datalink in ${datalink[@]}; do
    export PGPASSWORD=mysecrestpassword
    psql -U postgres -d offchaindb -h $datalink -c "drop database iroha_default;"
done

exit $?