import db_config, db_connection

db = db_connection.OracleDB(db_config.user, db_config.passwd, db_config.server, db_config.port, db_config.sid)
db.connect()

cursor = db.cursor.execute("SELECT * FROM permissao")
for result in cursor:
    print(result)
db.close()