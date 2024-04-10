import serial
import time

# Replace this with your serial port name
serial_port = '/dev/cu.usbmodem1101'
baud_rate = 115200  # In arduino, Serial.begin(baud_rate)

try:
    with serial.Serial(serial_port, baud_rate) as ser:
        while True:
            line = ser.readline()  # .decode('utf-8').rstrip()
            print(line)
            time.sleep(0.1)
except serial.SerialException as e:
    print("Error:", e)


