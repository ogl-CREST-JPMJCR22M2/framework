import psycopg2
from psycopg2 import Error

connector=psycopg2.connect(
        host="localhost",
        database="iroha_default",
        user="postgres",
        password="mysecretpassword"
)

cur = connector.cursor()

cur.execute("""
        insert into test values('e01001','0.0')
""")

connector.commit()