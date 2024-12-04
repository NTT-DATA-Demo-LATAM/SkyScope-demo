from flask import render_template, request
from . import app
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_APPID')

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None

    if request.method == 'POST':
        city = request.form['city']

        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}'

        response = requests.get(url).json()

        temperature_kelvin = response['main']['temp']
        temperature_celsius = round(temperature_kelvin - 273.15, 1)

        weather = {
            'country': response['sys']['country'],
            'city': response['name'],
            'temperature': temperature_celsius,
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon'],
            'wind_speed': response['wind']['speed'],
            'rain': response.get('rain', {}).get('1h', 0),
            'pressure': response['main']['pressure'],
            'visibility': response.get('visibility', 'N/A'),
            'snow': response.get('snow', {}).get('1h', 0)
        }

    return render_template('index.html', weather=weather)
