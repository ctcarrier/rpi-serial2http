import serial
from xbee import XBee

ser = serial.Serial('/dev/ttyAMA0')
xbee = XBee(ser)

while True:
    rcv = ser.read(21)
    print(str(rcv).encode('hex'))
    parsed = xbee._split_response(rcv)
    print(parsed)