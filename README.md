# flask-oracle
Connection test using oracle

## Instalação e utilização

Requer python 3.4 e pipenv

* Crie o ambiente virtual `python3 -m venv .venv`
* Ative o ambiente virtual
    * Windows `.venv\Scripts\activate`
    * Linux ou Mac `source .venv\bin\activate`
* Instale as dependências `pipenv install`
* Crie o arquivo de configuração `.env` ([Exemplo](#configuracao))
* Rode a aplicação `python src/processo_automatico.py`




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


##### Create a .env file 
```
DB_USER = "user"  
DB_PASSWD = "password"  
DB_DSN = "0.0.0.0/oracledb"  
DB_SERVER = "0.0.0.0"  
DB_PORT = port number  
DB_SID = "yoursid"  
```


## Configuration

| Atributo | Descrição | Exemplo |
| --- | --- | --- |
|DB_HOST | Endereço do banco | 192.168.0.10 ou banco.seudominio.com |

