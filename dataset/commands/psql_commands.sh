psql -U postgres -d iroha_default -h postgresA -c "delete from cfpval;"

psql -U postgres -d offchaindb -h postgresA -c "\copy offchaindb_cfpval (partsid, totalcfp, cfp) from '/root/dataset/init/A10000.csv' with csv header;"
psql -U postgres -d offchaindb -h postgresB -c "\copy offchaindb_cfpval (partsid, totalcfp, cfp) from '/root/dataset/init/B10000.csv' with csv header;"
psql -U postgres -d offchaindb -h postgresC -c "\copy offchaindb_cfpval (partsid, totalcfp, cfp) from '/root/dataset/init/C10000.csv' with csv header;"

psql -U postgres -d offchaindb -h postgresA -c "\copy offchaindb_cfpval (partsid, totalcfp, cfp) from '/root/results/Acfpval.csv' with csv header;"
psql -U postgres -d offchaindb -h postgresB -c "\copy offchaindb_cfpval (partsid, totalcfp, cfp) from '/root/results/Bcfpval.csv' with csv header;"
psql -U postgres -d offchaindb -h postgresC -c "\copy offchaindb_cfpval (partsid, totalcfp, cfp) from '/root/results/Ccfpval.csv' with csv header;"

psql -U postgres -d iroha_default -h postgresA -c "\copy cfpval (partsid, totalcfp) from '/root/results/cfpval.csv' with csv header;"
psql -U postgres -d iroha_default -h postgresB -c "\copy cfpval (partsid, totalcfp) from '/root/results/cfpval.csv' with csv header;"
psql -U postgres -d iroha_default -h postgresC -c "\copy cfpval (partsid, totalcfp) from '/root/results/cfpval.csv' with csv header;"
