#!/bin/bash

export PGPASSWORD=mysecretpassword

datalink=("postgresA" "postgresB" "postgresC")

for datalink in ${datalink[@]}; do
    psql -U postgres -d postgres -h $datalink -c "drop table offchaindb_cfpval;"
done

exit $?