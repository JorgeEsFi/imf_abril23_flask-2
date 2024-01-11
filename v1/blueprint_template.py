# Importar las librerías básicas de flask
from flask import Blueprint, jsonify, request

# Crear e inicializar el Blueprint
plantilla = Blueprint('NOMBRE_PLANTILLA', __name__)

# Asignarle una ruta base
baseURL = '/v1/AQUI_TU_RUTA/'

@plantilla.route(baseURL + 'test', methods=['GET'])
def plantilla_test():
    
    return jsonify({'result': True, 'response': 'Este es mi primer endpoint con Flask'}), 200