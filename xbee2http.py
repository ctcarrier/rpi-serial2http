#!/usr/bin/env python

import serial
from xbee import XBee
import requests
import datetime
import os

serial_port = serial.Serial('/dev/ttyAMA0', 9600)
xbee = XBee(ser = serial_port, escaped = True)

url = 'http://192.168.0.103:9090/api/sensorReadings'

user = os.environ['MT_USER']
password = os.environ['MT_PASSWORD']
tag = os.environ['SENSOR_TAG']

while True:
    try:
        data = xbee.wait_read_frame()
        data_split = data['rf_data'].split(',', 2)
        humidity = int(data_split[0])
        temp = int(data_split[1])
        timestamp = datetime.datetime.now().isoformat() + 'Z'
        payload = {'humidity': humidity, 'fahrenheit': temp, 'tag': tag, 'timestamp': timestamp}
        r = requests.post(url, json=payload, auth=(user, password))
        print(r.status_code)
        print(r.text)
    except KeyboardInterrupt:
        break

serial_port.close()