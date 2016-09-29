import serial

ser = serial.Serial('/dev/ttyUSB0')

while True:
    rcv = ser.read(10)