import requests
import os
import datetime

url = 'http://192.168.0.103:9090/api/sensorReadings'

user = os.environ['MT_USER']
password = os.environ['MT_PASSWORD']

timestamp = datetime.datetime.now().isoformat() + 'Z'
payload = {'humidity': 70, 'fahrenheit': 60, 'tag': 'test', 'timestamp': timestamp}

r = requests.post(url, json=payload, auth=(user, password))
print(r.status_code)
print(r.text)