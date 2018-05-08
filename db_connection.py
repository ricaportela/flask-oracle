"""
    Oracle database connection
    @author: Ricardo Portela
"""
import cx_Oracle
# from sqlalchemy import create_engine
# import sqlalchemy.pool as pool
from decouple import config


class OracleDB:
    """
       OracleDB Connection
    """
    def __init__(self):
        self.user = config('DB_USER')
        self.password = config('DB_PASSWORD')
        self.server = config('DB_SERVER')
        self.port = config('DB_PORT')
        self.sid = config('DB_SID')
        self.tns = cx_Oracle.makedsn(self.server, self.port, self.sid)
        self.connection = None
        self.cursor = None
        self.engine = None
        self.mypool = None
        self.connect()

    def connect(self):
        self.tns = cx_Oracle.makedsn(self.server, self.port, service_name=self.sid)

        try:
            self.connection = cx_Oracle.connect(self.user, self.password, self.tns)
            print("conectou...")

        except cx_Oracle.DatabaseError as e:
            self.connection = None
            print(e)
            exit(1)

        # self.engine = create_engine(self.connection)

        self.cursor = self.connection.cursor()

    def connection_close(self):
        self.connection.close()


if __name__ == '__main__':
    ora = OracleDB()
    # mypool = pool.QueuePool(ora, max_overflow=10, pool_size=5)
    # get a connection
    # conn = mypool.connect()

    cursor = ora.cursor.execute("SELECT * FROM permissao")
    for result in cursor:
        print(result)
    ora.connection_close()
