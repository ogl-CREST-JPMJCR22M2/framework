#!/bin/bash

export PGPASSWORD=mysecretpassword

datalink=("postgresA" "postgresB" "postgresC")

for datalink in ${datalink[@]}; do
    export PGPASSWORD=mysecrestpassword
    psql -U postgres -d iroha_default -h $datalink -c "drop database irofa_default;"
done

exit $?