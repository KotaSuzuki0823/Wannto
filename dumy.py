import serial
import sys

try:
    conn = serial.Serial("tty.raspberrypi-SerialPort", baudrate=9600, timeout=5)
    print('import tty.raspberrypi-SerialPort')
except Exception as e:
    sys.exit("\n%s" % str(e))

try:
    conn.write('1')
except Exception as e:
    sys.exit("Oops! %s\n" % str(e))

print("send request. start receive..")

data = conn.read(2000000)#2MB
print("書き込みます")
with open("image.jpg", 'wb') as img:
    img.write(data)