#!/usr/bin/env python

import serial
from xbee import ZigBee
import requests
import datetime
import os
import logging

serial_port = serial.Serial('/dev/serial0', 9600)
xbee = ZigBee(ser = serial_port, escaped = True)

LOG_FILENAME = '/var/log/xbeedebug.log'

logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO, format='%(asctime)s %(message)s')
logging.info('Started %s' % __file__)

while True:
    try:
        # data = xbee.wait_read_frame()
        # data_split = data['rf_data'].split(',', 2)
        # logging.info(data['rf_data'])
        # print(data['rf_data'])
        rcv = serial_port.read(21)
        print(str(rcv).encode('hex'))
    except KeyboardInterrupt:
        break

serial_port.close()