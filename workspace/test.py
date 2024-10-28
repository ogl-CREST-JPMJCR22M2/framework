#Naive
explain analyze WITH
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
        WHERE general_table.parents_partsid = 'P00001'
        UNION ALL
        SELECT general_table.partsid, calcu.parents_partsid, cfp
        FROM general_table, calcu
        WHERE general_table.parents_partsid = calcu.child_partsid 
    )
    SELECT parents_partsid, SUM(totalcfp) AS child_totalcfp
    FROM calcu
    GROUP BY parents_partsid
)
SELECT cfp, child_totalcfp + cfp as new_Totalcfp
FROM get_totalcfp, import_table
WHERE get_totalcfp.parents_partsid= 'P00001' AND import_table.partsid =  'P00001';



#Quick
explain analyze VERBOSE WITH
import_table AS 
(
    SELECT * FROM dblink(
        'host=' || (SELECT DataLink FROM PartsInfo WHERE PartsID = 'P00001') || ' port=5432 dbname=offchaindb user=postgres password=mysecretpassword', 
        'SELECT partsid, cfp FROM offchaindb_cfpval') 
        AS t1(partsid CHARACTER varying(288), cfp DECIMAL)
),
general_table AS
(   
    SELECT * FROM cfpval
    NATURAL RIGHT JOIN PartsInfo
),
get_totalcfp AS
(
    SELECT parents_partsid, SUM(totalcfp) AS child_totalcfp
        FROM general_table
        GROUP BY parents_partsid
)
SELECT cfp, child_totalcfp + cfp as new_Totalcfp
FROM get_totalcfp, import_table
WHERE get_totalcfp.parents_partsid='P00001' AND import_table.partsid = 'P00001';




explain analyze WITH
get_childparts AS
(
    WITH RECURSIVE calcu(child_partsid, parents_partsid) AS
    (
        SELECT PartsInfo.partsid, PartsInfo.parents_partsid 
        FROM PartsInfo
        WHERE PartsInfo.parents_partsid = 'P09841'
        UNION ALL
        SELECT PartsInfo.partsid, calcu.parents_partsid
        FROM PartsInfo, calcu
        WHERE PartsInfo.parents_partsid = calcu.child_partsid 
    )
    SELECT child_partsid
    FROM calcu
),
import_table AS (
    SELECT * FROM dblink(
        'host=postgresA port=5432 dbname=offchaindb user=postgres password=mysecretpassword', 
        'SELECT partsid, cfp FROM offchaindb_cfpval') 
        AS t1(partsid CHARACTER varying(288), cfp DECIMAL)
    UNION ALL
    SELECT * FROM dblink(
        'host=postgresB port=5432 dbname=offchaindb user=postgres password=mysecretpassword', 
        'SELECT partsid, cfp FROM offchaindb_cfpval') 
        AS t1(partsid CHARACTER varying(288), cfp DECIMAL)
    UNION ALL
    SELECT * FROM dblink(
        'host=postgresC port=5432 dbname=offchaindb user=postgres password=mysecretpassword', 
        'SELECT partsid, cfp FROM offchaindb_cfpval') 
        AS t1(partsid CHARACTER varying(288), cfp DECIMAL)
),
get_totalcfp AS
(   
    SELECT sum(cfp) as child_totalcfp
    FROM import_table INNER JOIN get_childparts ON get_childparts.child_partsid=import_table.partsid
)
SELECT import_table.cfp, child_totalcfp + import_table.cfp as new_Totalcfp
FROM get_totalcfp, import_table
WHERE import_table.partsid =  'P09841';
