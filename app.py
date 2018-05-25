from flask import Flask
from flask import request, jsonify, render_template
from database import OracleDB

app = Flask('app')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clientqty/')
def test():
    ora = OracleDB()
    ora.connect()
    l_res = ora.clientesqty()
    print(l_res)
    return jsonify(l_res)

@app.route('/camerabyidcli/')
def test0():
    ora = OracleDB()
    ora.connect()
    l_res = ora.camerabyclientid(701)
    return l_res

@app.route('/permissoes/', methods=['GET', 'POST'])
def test1():    
    ora = OracleDB()
    ora.connect()
    ora.resultado()
    l_res = ora.resultado()
    return l_res

@app.route('/clientesids/')
def test2():
    ora = OracleDB()
    ora.connect()
    l_res = ora.clientesids()
    return l_res

    

@app.errorhandler(500)
def handle_500(error):
    return str(error), 500


if __name__ == '__main__':
    app.run()