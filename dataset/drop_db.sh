#!/bin/bash

export PGPASSWORD=mysecrestpassword

dabalink=("postgresA" "postgresB" "postgresC")

for dabalink in ${dabalink[@]}; do
    psql -U postgres -d postgres -h $dabalink -c "drop database irofa_default;"
done

exit $?