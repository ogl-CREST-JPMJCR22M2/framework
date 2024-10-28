WITH
            import_tableA AS 
            (
                SELECT * FROM dblink(
                    'host=postgresA port=5432 dbname=offchaindb user=postgres password=mysecretpassword', 
                    'SELECT partsid, cfp FROM offchaindb_cfpval') 
                    AS t1(partsid CHARACTER varying(288), cfp DECIMAL)
             ),
            import_tableB AS
            (
                SELECT * FROM dblink(
                    'host=postgresB port=5432 dbname=offchaindb user=postgres password=mysecretpassword', 
                    'SELECT partsid, cfp FROM offchaindb_cfpval') 
                    AS t1(partsid CHARACTER varying(288), cfp DECIMAL)
            ),
            import_tableC AS
            (
                SELECT * FROM dblink(
                    'host=postgresC port=5432 dbname=offchaindb user=postgres password=mysecretpassword', 
                    'SELECT partsid, cfp FROM offchaindb_cfpval') 
                    AS t1(partsid CHARACTER varying(288), cfp DECIMAL)
            ),
            import_table AS
            (
                SELECT * FROM import_tableA
                UNION
                SELECT * FROM import_tableB
                UNION
                SELECT * FROM import_tableC
            ),
            general_table AS
            (   
                SELECT * FROM import_table
                NATURAL RIGHT JOIN PartsInfo
            ),
            get_totalcfp AS
            (
                WITH RECURSIVE calcu(child_partsid, parents_partsid, totalcfp) AS
                (
                  SELECT general_table.partsid, general_table.parents_partsid, general_table.cfp 
                   FROM general_table
                  UNION ALL
                  SELECT general_table.partsid, calcu.parents_partsid, cfp
                   FROM general_table, calcu
                   WHERE general_table.parents_partsid = calcu.child_partsid
                )
                SELECT parents_partsid, SUM(totalcfp) AS child_totalcfp
                 FROM calcu
                 GROUP BY parents_partsid
            ),
            new_quantity AS
             (
                 SELECT cfp, child_totalcfp + cfp as new_Totalcfp
                  FROM get_totalcfp, import_table
                  WHERE get_totalcfp.parents_partsid='P00500' AND import_table.partsid = 'P00500'
             )
             select * from new_quantity;