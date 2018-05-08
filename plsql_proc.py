import cx_Oracle
import db_config

con = cx_Oracle.connect(db_config.user, db_config.passwd, db_config.dsn)

cur = con.cursor()

myvar = cur.var(int)
cur.callproc('myproc', (177700, myvar))
print(myvar.getvalue())