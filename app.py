from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import requests
import os

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.3')

@app.route('/')
def get_weather():
    api_key = os.environ.get('WEATHER_API_KEY')
    if not api_key:
        return jsonify({'error': 'API key not found'}), 500
    city = "Moscow"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    data = requests.get(url).json()
    temperature = data['main']['temp']
    condition = data['weather'][0]['main']
    return jsonify({
        'city': city,
        'temperature': temperature,
        'condition': condition,
        'status': 'ok'
    })

@app.route('/health')
@metrics.do_not_track()
def health_check():
    return jsonify({'status': 'up'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)