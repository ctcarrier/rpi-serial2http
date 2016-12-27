#!/usr/bin/env python

import serial
from xbee import ZigBee
import requests
import datetime
import os
import logging

serial_port = serial.Serial('/dev/serial0', 9600)
xbee = ZigBee(ser = serial_port, escaped = True)

user = os.environ['MT_USER']
password = os.environ['MT_PASSWORD']
host = os.environ['MT_HOST']

url = 'http://' + host + '/api/sensorReadings'
LOG_FILENAME = '/var/log/xbee2http.log'

logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO, format='%(asctime)s %(message)s')
logging.info('Started %s' % __file__)

def convertRawData(d):
    return int(d) / 100


while True:
    try:
        data = xbee.wait_read_frame()

        source_addr_long = data['source_addr_long']
        rf_data = data['rf_data']
        if source_addr_long is None or rf_data is None:
            print('Not a data packet')
            print(data)
        else:
            split_data = rf_data.split(',')
            print(rf_data)
            print(split_data)
            print(source_addr_long.encode('hex'))
            sensor = split_data[0]
            sensor_data = map(convertRawData, split_data[1:])
            timestamp = datetime.datetime.now().isoformat() + 'Z'
            payload = \
                {
                    'sensor': sensor,
                    'sensorData': sensor_data,
                    'sourceAddress': source_addr_long.encode('hex'),
                    'timestamp': timestamp
                }

            logging.info(payload)
            r = requests.post(url, json=payload, auth=(user, password))
            logging.info(r.status_code)
            logging.info(r.text)

    except KeyboardInterrupt:
        break

serial_port.close()