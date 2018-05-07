"""
    Oracle database connection
    @author: Ricardo Portela
"""
import cx_Oracle


class OracleDB:
    """
       OracleDB Connection
    """
    def __init__(self, user, password, server, port, sid):
        self.tns = cx_Oracle.makedsn(server, port, sid)
        self.connection = None
        self.cursor = None
        self.user = user
        self.password = password

    def connect(self):
        try:
            self.connection = cx_Oracle.connect(self.user, self.password, self.tns)
            print("conectou...")
        except cx_Oracle.DatabaseError as e:
            print('Failed to connect to %s\n', self.tns)
            # printException(exception)
            exit(1)
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()

