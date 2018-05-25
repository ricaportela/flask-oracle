"""DBORacle."""
# db1 = cx_Oracle.connect('desenv/devquality@192.168.1.10:1521/orcldev')
# dsn_tns = cx_Oracle.makedsn('192.168.1.10', 1521, 'orcldev')
# db = create_engine("oracle+cx_oracle://desenv: \
#             devquality@192.168.1.10/orcldev", pool_size=20)
# db = cx_Oracle.connect('desenv', 'devquality', '192.168.1.10:1521/orcldev')
import cx_Oracle
import datetime

conn = cx_Oracle.connect('desenv/devquality@192.168.1.10:1521/orcldev')

array_sizes = (50, 500, 5000)

sql = 'select * from cliente'
for size in array_sizes:
    cursor = conn.cursor()
    cursor.arraysize = size
    start_time = datetime.datetime.today()
    results = cursor.execute(sql).fetchall()
    end_time = datetime.datetime.today()
    cursor.close()
    print("Consultando... {}".format(size), end_time - start_time)

conn.close()
