import serial
from xbee import XBee

serial_port = serial.Serial('/dev/ttyAMA0', 9600)
xbee = XBee(serial_port)

while True:
    try:
        data = xbee.wait_read_frame()
        print(data)
    except KeyboardInterrupt:
        break

serial_port.close()