import serial
from xbee import XBee

ser = serial.Serial('/dev/ttyAMA0')
xbee = XBee(ser)

while True:
    frame = APIFrame(escaped=self._escaped)
    rcv = ser.read(21)
    print(str(rcv).encode('hex'))
    for b in rcv:
        frame.fill(b)

    frame.parse()
    parsed = xbee._split_response(frame)
    print(parsed)