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
    except KeyboardInterrupt:
        break

serial_port.close()