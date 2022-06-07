from re import T
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hola amiguito soy BOt-ella'

@app.route('/proces')
def proceso():
    return 'Se desatara el proceso'

@app.route('/param')
#http://127.0.0.1:5600/param?ruta=%22c:/ca/reat/%22&archivo=foto.jpg
def paramemtro():
    n_param = request.args.get('ruta','No definida')
    n_archivo =request.args.get('archivo','no definido')
    n_tolerancia =request.args.get('tolerancia','no definido')
    salida =f"usted ejecuto con los siguientes parametros ruta {n_param} , archivo {n_archivo} y tolerancia {n_tolerancia}"
    return salida

@app.route('/config')
@app.route('/config/<n_ruta>/')
@app.route('/config/<n_ruta>/<n_archivo>')
#http://127.0.0.1:5600/config/carpeta/foto.jpg
def config(n_ruta='No definida',n_archivo ='no definido'):
    salida =f"usted ejecuto config con ruta {n_ruta} y archivo {n_archivo}"
    return salida
if __name__ == '__main__':
    app.run(debug=True,port= 5600)

