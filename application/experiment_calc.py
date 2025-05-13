from sqlalchemy import create_engine
import polars as pl
import time
import random
import hashlib
from decimal import *
from psycopg2 import connect, sql

import calculation as c
import SQLexecutor as SQLexe
import write_to_db as w
import v as v
import u as u


peers = ["postgresA", "postgresB", "postgresC"]

root_partid = 'P0'
assembler = w.get_Assebler(root_partid)
c.make_merkltree(assembler, root_partid)

#id = ["P1","P2", "P3", "P4", "P5"]
#id = ["P30", "P12", "P6", "P15", "P10"]
#id = ["P35", "P120", "P110", "P50", "P153"]
#id = ["P770", "P305", "P400", "P35", "P57"]
#id = ["P900", "P1200", "P2000", "P3800", "P2500"]
id = ["P11350", "P12100", "P2000", "P3800", "P19000"]


for i in range(5):

    target_partid = id[i]
    assembler = w.get_Assebler(target_partid)

    start = time.time()

    u.make_merkltree(assembler, target_partid, 0.1717)
    
    t = time.time() - start
    print("time:", t)
    
        