"""
    Oracle database connection
    @author: Ricardo Portela
"""
import cx_Oracle
from sqlalchemy import create_engine
from decouple import config


class OracleDB:
    """
       OracleDB Database
    """
    def __init__(self):
        self.username = config('DB_USER')
        self.password = config('DB_PASSWORD')
        self.hostname = config('DB_SERVER')
        self.port = config('DB_PORT')
        self.sid = config('DB_SID')
        self.engine = None
        self.conn = None
        self.rconn = None
        self.oracle_connection_string = None
        # self.oracle_connection_string = ('oracle+cx_oracle://{self.username}:{self.password}@' +
        #     cx_Oracle.makedsn('{self.hostname}', '{self.port}', service_name='{self.sid}')
        # )

    def connect(self):
        try:
            self.engine = create_engine(
                self.oracle_connection_string.format(
                    username=self.username,
                    password=self.password,
                    hostname=self.hostname,
                    port=self.port,
                    service_name=self.sid,
                ), pool_size=20)
            self.conn = self.engine.connect()
            print("conectou...")
        except cx_Oracle.DatabaseError as e:
            self.engine = None
            print(e)
            exit(1)

    def resultado(self):
        result = self.conn.execute("SELECT * FROM permissao")
        for result in result:
            print(result)

    def cameras(self):
        rconn = self.engine.raw_connection()
        cur = rconn.connection.cursor()
        l_cur = cur.var(cx_Oracle.CURSOR)
        res = cur.callproc('PKG_CAMERA.PRC_SELECT_CAMERA_QTY_BY_CLIENT', (701, l_cur))
        res = l_cur.getvalue().fetchall()
        print(res[0][1])

    def connection_close(self):
        self.conn.close()
        print("Fechou...")


if __name__ == '__main__':
    ora = OracleDB()
    ora.connect()
    ora.cameras()
    ora.connection_close()








# from sqlalchemy import create_engine
# import cx_Oracle
# from decouple import config


# try:
#     engine = create_engine('oracle+cx_oracle://desenv:devquality@192.168.1.10/orcldev', pool_size=100)
#     conn = engine.connect()
#     rconn = engine.raw_connection()
#     cur = rconn.connection.cursor()
#     l_cur = cur.var(cx_Oracle.CURSOR)
#     res = cur.callproc('PKG_CAMERA.PRC_SELECT_CAMERA_QTY_BY_CLIENT', (701, l_cur))
#     res = l_cur.getvalue().fetchall()
#     print(res[0][1])
# except Error as e:
#     print(e)
# finally:
#     rconn.close()
#     conn.close()
