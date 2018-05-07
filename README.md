# flask-oracle
Connection test using oracle


# Install Oracle drivers on SO
https://oracle.github.io/odpi/doc/installation.html#linux


1) Download the instantclient-basic-linux.x64-12.2.0.1.0.zip

2) Extract it to /opt/oracle directory:

``` sudo mkdir -p /opt/oracle ```
``` cd /opt/oracle ```
``` unzip ~/Downloads/instantclient-basic-linux.x64-12.2.0.1.0.zip ```

3) Install libaio package

```sudo apt-get install libaio1```

4) Edit the oracle-instantclient.conf file like so:

``` sudo sh -c "echo /opt/oracle/instantclient_12_2 > /etc/ld.so.conf.d/oracle-instantclient.conf" ```
``` sudo ldconfig ```


##### Create file db_config.py
user = "user"
passwd = "password"
dsn = "0.0.0.0/oracledb"
server = "0.0.0.0"
port = port number
sid = "yoursid"

