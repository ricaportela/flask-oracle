"""
    Oracle database connection
    @author: Ricardo Portela
"""
import cx_Oracle
from sqlalchemy import create_engine
from decouple import config
from pprint import pprint
import datetime
from flask import jsonify


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
                ), pool_size=100)
            self.conn = self.engine.connect()
            self.rconn = self.engine.raw_connection()
            print("conectou...")

        except cx_Oracle.DatabaseError as e:
            self.engine = None
            print(e)
            exit(1)

    def resultado(self):
        res = self.conn.execute("SELECT * FROM permissao")
        payload = []
        content = {}
        for result in res:
            content = {'id': result[0], 'username': result[1]}
            payload.append(content)
            content = {}
        return jsonify(payload)

    def camerabyclientid(self, l_number_start):
        cur = self.rconn.connection.cursor()
        l_cur = cur.var(cx_Oracle.CURSOR)
        cur.callproc('PKG_CAMERA.PRC_SELECT_CAMERA_QTY_BY_CLIENT', (l_number_start, l_cur))
        l_res = l_cur.getvalue().fetchall()
        payload = []
        content = {}
        for result in l_res:
            content = {'id_cliente': result[0], 'id_camera': result[1]}
            payload.append(content)
            content = {}
        return jsonify(payload)

    def clientesqty(self):
        cur = self.rconn.connection.cursor()
        l_cur = cur.var(cx_Oracle.CURSOR)
        res = cur.callproc('PKG_CLIENTE.PRC_SELECT_CLIENT_QTY', [0, ])
        return res

    def clientesids(self):
        cur = self.rconn.connection.cursor()
        l_cur = cur.var(cx_Oracle.CURSOR)
        res = cur.callproc('PKG_CLIENTE.PRC_SELECT_CLIENT_IDS', [l_cur])
        list_ids = l_cur.getvalue().fetchall()

        payload = []
        content = {}
        for result in list_ids:
            content = {'id_cliente': result[0]}
            payload.append(content)
            content = {}
        return jsonify(payload)

    def clientall(self):

        array_sizes = (100, 1000, 5000)

        sql = 'select * from cliente'
        for size in array_sizes:
            cursor = self.rconn.cursor()
            cursor.arraysize = size
            start_time = datetime.datetime.today()
            results = cursor.execute(sql).fetchall()
            end_time = datetime.datetime.today()
            cursor.close()
            print("Consultando... {}".format(size), end_time - start_time)

        return True

    def connection_close(self):
        self.conn.close()
        print("Fechou...")


# if __name__ == '__main__':
#     ora = OracleDB()
#     ora.connect()
#     ora.clientall()
#     ora.connection_close()
