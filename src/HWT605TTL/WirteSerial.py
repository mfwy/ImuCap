import serial
import struct
import time
import numpy as np
import matplotlib.pyplot as plt

SerialPort=serial.Serial("/dev/ttyUSB0",baudrate=115200,timeout=1)
unlock_cmd=b'\xff\xaa\x69\x88\xb5'

read_cmd=b'\xff\xaa\x27\x6a\x00'
rate_cmd=b'\xff\xaa\x03\x09\x00'
baud_cmd=b'\xff\xaa\x04\x06\x00'
acc_cali_cmd=b'\xff\xaa\x01\x01\x00'
gryo_cali_cmd=b'\xff\xaa\x61\x01\x00'
integr_cmd=b'\xff\xaa\x6e\xff\xff'


save_cmd=b'\xff\xaa\x00\x00\x00'

SerialPort.write(unlock_cmd)
time.sleep(0.2)

SerialPort.write(gryo_cali_cmd)
time.sleep(3)

SerialPort.write(save_cmd)
time.sleep(0.1)

data=SerialPort.read(600)

print(data)