"""DBSqlalchemy."""
import sqlalchemy

oracle_db = sqlalchemy.create_engine('oracle://desenv/devquality@192.168.1.10:1521/orcldev')

conn = oracle_db.connect()
result = conn.execute('select * from cliente')
for line in result:
    print(line)
