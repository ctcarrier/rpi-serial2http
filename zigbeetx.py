#!/usr/bin/env python

import serial
from xbee import ZigBee
import requests
import datetime
import os
import logging
from decimal import Decimal
import RPi.GPIO as GPIO
from threading import Timer

humidity_running = False
humidity_start_time = -1

serial_port = serial.Serial('/dev/serial0', 9600)
xbee = ZigBee(ser = serial_port, escaped = True)

GPIO.setmode(GPIO.BCM)
RELAY = 17
GPIO.setup(RELAY,GPIO.OUT)

user = os.environ['MT_USER']
password = os.environ['MT_PASSWORD']
host = os.environ['MT_HOST']

url = 'http://' + host + '/api/sensorReadings'
LOG_FILENAME = '/var/log/xbee2http.log'

logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO, format='%(asctime)s %(message)s')
logging.info('Started %s' % __file__)

HUMIDITY_LOW = 87
HUMIDITY_HIGH = 94
SOURCE_ADDR = '0013a200410464c0'
SENSOR_NAME = 'HX93'

CO2_LOW = 600
CO2_HIGH = 700
GAS_SENSOR_NAME = '22DTM51'

VENTILATION_DEST_ADDR_LONG = "\x00\x13\xA2\x00\x41\x04\x64\x4F"
VENTILATION_DEST_ADDR = "\xFF\xFE"
VENTILATION_ON_DATA = "\xFF"
VENTILATION_OFF_DATA = "\x00"

xbee.tx(frame='0x1', dest_addr_long=VENTILATION_DEST_ADDR_LONG, dest_addr=VENTILATION_DEST_ADDR, data="\x00")

def convertRawData(d):
    return float(d) / 100

humidifier_delay = datetime.timedelta(seconds=300)
humidifier_start = datetime.datetime.now() - humidifier_delay
humidifier_stop = datetime.datetime.now() - humidifier_delay

class humidity_timer():
    def __init__(self):
        logging.info('timer comes alive')
        self.timer = None
    def start(self):
        self.timer = Timer(60,self.relay_off)
        humidity_running = True
        humidifier_start = datetime.datetime.now()
        logging.info('humidity timer on')
        GPIO.output(RELAY,True)
        self.timer.start()
    def relay_off(self):
        logging.info('humidity timer off')
        humidity_running = False
        global humidifier_stop
        humidifier_stop = datetime.datetime.now()
        logging.info(humidifier_stop)
        GPIO.output(RELAY,False)
    def is_alive(self):
        logging.info(self.timer)
        logging.info(self.timer is not None)
        if self.timer is not None:
            return self.timer.is_alive()
        else:
            return False

htimer = humidity_timer()

while True:
    try:
        data = xbee.wait_read_frame()


        logging.info(data)
        rf_data = data['rf_data']
        source_addr_long = data['source_addr_long']
        if source_addr_long is None or rf_data is None:
            logging.error('Not a data packet')
            logging.error(data)
        else:
            split_data = rf_data.split(',')
            print(rf_data)
            print(split_data)
            print(source_addr_long.encode('hex'))
            sensor = split_data[0]
            sensor_data = map(convertRawData, split_data[1:])
            timestamp = datetime.datetime.now().isoformat() + 'Z'
            sourceAddress = source_addr_long.encode('hex')
            payload = \
                {
                    'sensor': sensor,
                    'sensorData': sensor_data,
                    'sourceAddress': sourceAddress,
                    'timestamp': timestamp
                }

            logging.info(payload)
            r = requests.post(url, json=payload, auth=(user, password))
            logging.info(r.status_code)
            logging.info(r.text)
            if sourceAddress == SOURCE_ADDR:
                logging.info(datetime.datetime.now())
                logging.info(humidifier_stop)
                logging.info(humidifier_delay)
                if (sensor == SENSOR_NAME) and ((datetime.datetime.now() - humidifier_stop) > humidifier_delay) :
                    if sensor_data[0] < HUMIDITY_LOW and not htimer.is_alive():
                        logging.info('Setting pin high')
                        htimer.start()

                    elif sensor_data[0] >= HUMIDITY_HIGH:
                        logging.info('Setting pin low')
                        GPIO.output(RELAY,False)
                elif sensor == GAS_SENSOR_NAME:
                    if sensor_data[2] < CO2_LOW:
                        logging.info('Ventilation off')
                        #xbee.tx(frame='0x1',
                        #    dest_addr_long=VENTILATION_DEST_ADDR_LONG,
                        #    dest_addr=VENTILATION_DEST_ADDR,
                        #    data=VENTILATION_OFF_DATA)
                    elif sensor_data[2] >= CO2_HIGH:
                        logging.info('Ventilation on')
                        #xbee.tx(frame='0x1',
                        #    dest_addr_long=VENTILATION_DEST_ADDR_LONG,
                        #    dest_addr=VENTILATION_DEST_ADDR,
                        #    data=VENTILATION_ON_DATA)

    except KeyboardInterrupt:
        break
    except Exception as e:
        logging.exception("An error occured, continuing")
        pass

serial_port.close()
