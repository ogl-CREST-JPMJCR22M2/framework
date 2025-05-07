from sqlalchemy import create_engine
import polars as pl
import time
import random
import hashlib
from decimal import *

import calculation as c
import SQLexecutor as SQLexe
import write_to_db as w
import update_cfp as u


root_partid = 'P0'
assembler = w.get_Assebler(root_partid)
#id = ["P30", "P12", "P6", "P15"]
#id = ["P35", "P120", "P110", "P50"]
#id = ["P305", "P400", "P35", "P57"]
#id = ["P350", "P1200", "P2000", "P3800"]
id = ["P11350", "P12100", "P2000", "P3800"]

for i in range(5):

    start = time.time()

    c.make_merkltree(assembler, root_partid, True)

    print("total:", time.time() - start)

    if i<4:
        assembler = w.get_Assebler(id[i])
        u.update_hash(assembler, id[i], random.random())
        