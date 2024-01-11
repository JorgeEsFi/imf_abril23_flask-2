from flask import Blueprint, jsonify, request
from .utils import functions

auth = Blueprint('auth', __name__)

baseURL = '/v1/auth/'

usuario_demo = "jorge"
password_demo = "dzWM9sXhe02dUBqBw2hyZPwxFeDW9vIs"


@auth.route(baseURL + 'login', methods=['POST'])
def login():
    
    try:
        inData = request.get_json()
        
        if inData['usuario'] == usuario_demo and inData['password'] == password_demo:
            return jsonify({'result': True, 'response': functions.auth.issue_jwt(inData['usuario'])}), 200
        else:
            return jsonify({'result': False, 'response': 'Usuario o contraseña incorrectos'}), 401
    
    except Exception as e:
        return jsonify({'result': False, 'response': f'Peticion malformada - {str(e)}'}), 400
    

@auth.route(baseURL + 'get_token', methods = ['POST'])
def get_token():
    try:
        inData = request.get_json()
        token = functions.auth.issue_jwt(inData)
        return jsonify({'result': True, 'response': token}), 200
    except:
        return jsonify({'result': False, 'response': 'Hubo un error general del token'}), 401
