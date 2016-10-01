import serial
from xbee import XBee

serial_port = serial.Serial('/dev/ttyAMA0', 9600)
xbee = XBee(ser = serial_port, escaped = True)

while True:
    try:
        data = xbee.wait_read_frame()
        data_split = data['rf_data'].split(',', 2)
        print(data_split[0])
        print(data_split[1])
    except KeyboardInterrupt:
        break

serial_port.close()