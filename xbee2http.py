import serial
from xbee import XBee
import requests
import datetime

serial_port = serial.Serial('/dev/ttyAMA0', 9600)
xbee = XBee(ser = serial_port, escaped = True)

url = 'http://192.168.0.103:9090/api/sensorReadings'

user = os.environ['MT_USER']
password = os.environ['MT_PASSWORD']

while True:
    try:
        data = xbee.wait_read_frame()
        data_split = data['rf_data'].split(',', 2)
        humidity = data_split[0]
        temp = data_split[1]
        timestamp = datetime.datetime.now().isoformat() + 'Z'
        payload = {'humidity': humidity, 'fahrenheit': temp, 'tag': 'test', 'timestamp': timestamp}
        r = requests.post(url, json=payload, auth=(user, password))
        print(r.status_code)
        print(r.text)
    except KeyboardInterrupt:
        break

serial_port.close()