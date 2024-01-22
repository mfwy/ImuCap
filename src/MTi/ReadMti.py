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


def get_head(buffer):
    return struct.unpack('>H',bytes(buffer))[0] 

def process(datalist):
    measurement={}
    j=0
    # print(len(datalist))
    while j<len(datalist)-5:
        field=get_head(datalist[j:j+2])
        if field==0x1020:
            j=j+5
        elif field==0x1060:
            timestamp=struct.unpack('>L',datalist[j+3:j+7])[0]
            # print(timestamp)
            measurement['timestamp']=timestamp
            j=j+7

        elif field==0x2033:
            j=j+27
        elif field==0x4023:
            # print("acc")
            acc=struct.unpack('>3d',datalist[j+3:j+27])
            measurement['acc']=acc
            j=j+27

        elif field==0x8023:
            # print("gyro")
            gyro=struct.unpack('>3d',datalist[j+3:j+27])
            measurement['gyro']=gyro
            j=j+27
            
        else:
            print("error")
    return measurement

if __name__=="__main__":
    global acc,gyro,timestamp
    SerialPort=serial.Serial("/dev/ttyUSB0",baudrate=921600,timeout=1)
    SerialPort.reset_input_buffer()
    start=time.time()
    rospy.init_node("mti",anonymous=True)
    pub=rospy.Publisher("/mti/imu",Imu,queue_size=10)
    rate=rospy.Rate(200)
    imu_msg=Imu()
    
    offset=0  #control the message flow offset
    byte_num=98 #default
    while not rospy.is_shutdown():
        data=SerialPort.read(offset+byte_num)
        new_data=[]
        
        for i in range(len(data)-3):
            if data[i]==0xfa and data[i+1]==0xff and data[i+2]==0x36:
                offset=i-offset
                byte_num=data[i+3]+5
                offset=byte_num-98+offset
                if offset>0:
                    print(data)
                    print(offset)
                    continue
                
                main_data=data[i+4:]
                # print(new_data)
                measurement=process(main_data)

                imu_msg.header.stamp=rospy.get_rostime()
                imu_msg.header.frame_id="base_link"
                imu_msg.linear_acceleration.x=measurement['acc'][0]
                imu_msg.linear_acceleration.y=measurement['acc'][1]
                imu_msg.linear_acceleration.z=measurement['acc'][2]

                imu_msg.angular_velocity.x=measurement['gyro'][0]
                imu_msg.angular_velocity.y=measurement['gyro'][1]
                imu_msg.angular_velocity.z=measurement['gyro'][2]
                # print(imu_msg.header.stamp)
                break
        pub.publish(imu_msg)
        rate.sleep()
        # end=time.time()
        # # print(end-start)
        # start=end
        



        


        
            
            
            
            





