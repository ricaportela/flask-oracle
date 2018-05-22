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
        self.oracle_connection_string = ('oracle+cx_oracle://{username}:{password}@' +
            cx_Oracle.makedsn('{hostname}', '{port}', service_name='{service_name}')
        )

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
    
    def camerasbyclientid(self):
        rconn = self.engine.raw_connection()
        cur = rconn.connection.cursor()
        l_cur = cur.var(cx_Oracle.CURSOR)
        res = cur.callproc('PKG_CAMERA.PRC_SELECT_CAMERA_QTY_BY_CLIENT', [701, l_cur])
        l_res = l_cur.getvalue().fetchall()
            
        return l_res

    def clientesqty(self):
        rconn = self.engine.raw_connection()
        cur = rconn.connection.cursor()
        l_cur = cur.var(cx_Oracle.CURSOR)
        res = cur.callproc('PKG_CLIENTE.PRC_SELECT_CLIENT_QTY', [0, ])
        return res

    def connection_close(self):
        self.conn.close()
        print("Fechou...")


if __name__ == '__main__':
    ora = OracleDB()
    ora.connect()
    print(ora.camerasbyclientid())
    print(ora.clientesqty())
    ora.connection_close()
