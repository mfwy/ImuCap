#!/usr/bin/env python3
import serial
import struct
import rospy
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from sensor_msgs.msg import Imu
import serial.tools.list_ports as slports
import subprocess

def find_ttyUSB():
    print('The default serial port of the imu is /dev/ttyUSB0')
    posts=[port.device for port in slports.comports() if 'USB' in port.device] #列表推导式
    print('Computer {} device {} total: {}'.format('USB', len(posts), posts))

def hex2short(data):
    return (struct.unpack('3h',bytes(data)))

if __name__=="__main__":
    global acc_x,acc_y,acc_z
    global gyro_x,gyro_y,gyro_z

    find_ttyUSB()
    rospy.init_node("hwt605",anonymous=True)
    pub=rospy.Publisher("/hwt605/imu",Imu,queue_size=10)
    imu_msg=Imu()
    rate=rospy.Rate(100)

    SerialPort=serial.Serial("/dev/ttyUSB0",baudrate=115200,timeout=1)
    start=time.time()

    while not rospy.is_shutdown():
        data=SerialPort.read(44)
        acc_flag=False
        gyro_flag=False
        i=-1
        while i<(len(data)-8):
            i+=1
            if data[i]==0x55 and data[i+1]==0x51 :
                m_acc=data[i+2:i+8]
                word=hex2short(m_acc)

                acc_x= word[0] / 32768*16*9.8
                acc_y= word[1] / 32768*16*9.8
                acc_z= word[2] / 32768*16*9.8
                acc_flag=True
                i+=10
            elif data[i]==0x55 and data[i+1]==0x52 :
                m_gyro=data[i+2:i+8]
                word=hex2short(m_gyro)

                gyro_x= word[0] / 32768*2000
                gyro_y= word[1] / 32768*2000
                gyro_z= word[2] / 32768*2000
                gyro_flag=True
                i+=10

            if acc_flag==True and gyro_flag==True:
                # end=time.time()
                # print("time cost:",end-start)
                # start=end
                # print(data)
                imu_msg.header.stamp=rospy.get_rostime()
                imu_msg.header.frame_id="base_link"
                
                imu_msg.linear_acceleration.x=acc_x
                imu_msg.linear_acceleration.y=acc_y
                imu_msg.linear_acceleration.z=acc_z

                imu_msg.angular_velocity.x=gyro_x
                imu_msg.angular_velocity.y=gyro_y
                imu_msg.angular_velocity.z=gyro_z
                break

        pub.publish(imu_msg)
        rate.sleep()
    

