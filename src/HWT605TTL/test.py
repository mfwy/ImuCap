import serial
import struct
import numpy as np
import matplotlib.pyplot as plt

SerialPort=serial.Serial("/dev/ttyUSB0",baudrate=9600,timeout=0.001)

plot_acc_x=[]
plot_acc_y=[]
plot_acc_z=[]
plot_gyro_x=[]
plot_gyro_y=[]
plot_gyro_z=[]
time=[]
time_g=[]
j=0
k=0
plt.ion()

while(True):
    data=SerialPort.read(121)

    for i in range(len(data)-11):
        if data[i]==0x55 and data[i+1]==0x51 :
            m_acc=data[i+2:i+8]

            word_x=struct.unpack('h',bytes([m_acc[0],m_acc[1]]))[0]
            word_y=struct.unpack('h',bytes([m_acc[2],m_acc[3]]))[0]
            word_z=struct.unpack('h',bytes([m_acc[4],m_acc[5]]))[0]

            acc_x= word_x / 32768*16*9.8
            acc_y= word_y / 32768*16*9.8
            acc_z= word_z / 32768*16*9.8
            plot_acc_x.append(acc_x)
            plot_acc_y.append(acc_y)
            plot_acc_z.append(acc_z)
            j=j+1
            time.append(j)
            plt.clf()
            plt.subplot(2,1,1)
            plt.plot(time,plot_acc_z)
            if j>100:
                plt.xlim(j-100,j+10)
            else:
                plt.xlim(1,110)
            plt.ylim(-15,15)
            plt.pause(0.001)
        # elif data[i]==0x55 and data[i+1]==0x52 :
        #     m_acc=data[i+2:i+8]

        #     word_x=struct.unpack('h',bytes([m_acc[0],m_acc[1]]))[0]
        #     word_y=struct.unpack('h',bytes([m_acc[2],m_acc[3]]))[0]
        #     word_z=struct.unpack('h',bytes([m_acc[4],m_acc[5]]))[0]

        #     gyro_x= word_x / 32768*2000
        #     gyro_y= word_y / 32768*2000
        #     gyro_z= word_z / 32768*2000
        #     plot_gyro_x.append(gyro_x)
        #     plot_gyro_y.append(gyro_y)
        #     plot_gyro_z.append(gyro_z)
        #     k=k+1
        #     time_g.append(k)

        #     plt.subplot(2,2,2)
        #     plt.plot(time_g,plot_gyro_x)
        #     if k>100:
        #         plt.xlim(k-100,k+10)
        #     else:
        #         plt.xlim(1,110)
        #     plt.ylim(-15,15)
        #     plt.pause(0.001)
            # plt.subplot(3,1,2)
            # plt.plot(time,plot_acc_y)
            # if j>100:
            #     plt.xlim(j-100,j+10)
            # else:
            #     plt.xlim(1,110)
            # plt.ylim(-15,15)

            # plt.subplot(3,1,3)
            # plt.plot(time,plot_acc_z)
            # if j>100:
            #     plt.xlim(j-100,j+10)
            # else:
            #     plt.xlim(1,110)
            # plt.ylim(-15,15)
            



        # plt.subplot(3,2,4)
        # plt.plot(time_g,plot_gyro_y)
        # if k>100:
        #     plt.xlim(k-100,k+10)
        # else:
        #     plt.xlim(1,110)
        # plt.ylim(-15,15)

        # plt.subplot(3,2,6)
        # plt.plot(time_g,plot_gyro_z)
        # if k>100:
        #     plt.xlim(k-100,k+10)
        # else:
        #     plt.xlim(1,110)
        # plt.ylim(-15,15)
            




        


        
