#!/bin/bash

export PGPASSWORD=mysecrestpassword

dabalink=("postgresA" "postgresB" "postgresC")

for dabalink in ${dabalink[@]}; do
    psql -U postgres -d offchaindb -h $dabalink -c "delete from offchaindb_cfpval;"
    psql -U postgres -d iroha_default -h $dabalink -c "delete from cfpval;"
    psql -U postgres -d iroha_default -h $dabalink -c "delete from partsinfo;"
done

exit $?