from flask import Blueprint, jsonify, request
from geopy.geocoders import Nominatim
import requests
from .utils import functions

open_weather = Blueprint('open_weather', __name__)

baseURL = '/v1/weather/'

@open_weather.route(baseURL + 'test', methods=['GET'])
def weather_test():
    
    return jsonify({'result': True, 'response': 'Este es mi primer endpoint con Flask'}), 200

@open_weather.route(baseURL + '7days/<_ciudad>', methods=['GET'])
def weather_7days(_ciudad):
    try:
        geolocator=Nominatim(user_agent="my_weather_application")
        location=geolocator.geocode(_ciudad)
        lat=location.latitude
        lon=location.longitude
        weather = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m")
    
        return jsonify({'result': True, 'response': weather}), 200
    except Exception as e:
        return jsonify({'result': False, 'response': f"Error en la solicitud {e}"}), 400

@open_weather.route(baseURL + '7days', methods=['POST'])
@functions.fence
def weather_7days_post():
    
    try:
        inData = request.get_json()
        headerAuth = request.headers['Authorization']
        
        jwtData = functions.auth.check_jwt(headerAuth.split(' ')[1])['response']
        
        query = f"SELECT * FROM movimientos_bancarios WHERE usuario = '{jwtData['user']}'"
        
        
        if inData['ciudad'] == '':
            return jsonify({'result': False, 'response': 'Debe ingresar una ciudad'}), 400
        else:
            
            geolocator = Nominatim(user_agent="imfTest")
            location = geolocator.geocode(inData['ciudad'])
            
            req = requests.get('https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&daily=temperature_2m_max,precipitation_sum&timezone=Europe%2FBerlin'.format(location.latitude, location.longitude))
            result = req.json()
            
            data = result['daily']
            
            weatherData = {}
            
            for i in range(len(data['time'])):
                weatherData[data['time'][i]] = {'temp': data['temperature_2m_max'][i], 'precipitacion': data['precipitation_sum'][i]}
            
            respuesta = {
                "user": jwtData['user'],
                "query": query,
                "city": {
                    "name": inData['ciudad'],
                    "lat": location.latitude, 
                    "lon": location.longitude
                },
                "weather": weatherData
                
            }
            
            return jsonify({'result': True, 'response': respuesta}), 200
    except Exception as e:
        return jsonify({'result': False, 'response': f'Peticion malformada - {str(e)}'}), 400

@open_weather.route(baseURL + 'mycity', methods=['POST'])
@functions.fence
def mycity():
    try:
        heatherAuth = request.headers['Authorization']
        jwt = functions.auth.check_jwt(heatherAuth.split(' ')[1])['response']
        return weather_7days(jwt['city'])
    except Exception as e:
        return jsonify({'result': False, 'response': f'Peticion malformada - {str(e)}'}), 400
