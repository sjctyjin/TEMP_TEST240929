import time
import serial
import struct

# 配置串行通訊參數
ser = serial.Serial(
    port='COM5',  # 這裡的端口號根據您的設備而定
    # port='/dev/ttyUSB0',  # 這裡的端口號根據您的設備而定
    baudrate=115200,        # 設置波特率
    parity='E',
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.1             # 讀取超時設置
)

"""Num1"""
ser.write(bytes([0x01, 0x06, 0x00, 0x10, 0x00, 0x90, 0x88, 0x63]))  # Start Num0

# 接收數據 Num1
received_data = ser.readline()  # 讀取10個字節的數據
print(received_data)
time.sleep(1)

"""Num0"""
ser.write( bytes([0x01, 0x06, 0x00, 0x10, 0x00, 0x91, 0x49, 0xA3]))  # Start Num1

# 接收數據 Num0
received_data = ser.readline()
print("Number : ",received_data)
time.sleep(1.5)
ser.write(bytes([0x01, 0x04, 0x00, 0x26, 0x00, 0x05, 0xd1, 0xc2]))  # Start Read
# ser.write( bytes([0x01, 0x04, 0x00, 0x24, 0x00, 0x02, 0x31, 0xC0]))  # Start Num1
# time.sleep(1)
# 接收數據 Num1
received_data = ser.read(200)
# data = ser.read(200)
print(received_data)

# data_disp=data.strip()#.decode('UTF-8')
# print(data_disp)
# print(received_data)
torque = struct.unpack('>H',received_data[3:5])
speed = struct.unpack('>H',received_data[5:7])
position = struct.unpack('>H',received_data[7:9])
voltage = struct.unpack('>H',received_data[9:11])
temperature = struct.unpack('>H',received_data[11:13])
#
print("扭力值 : ",torque)
print("速度 : ",speed)
print("位置 : ",position)
print("電壓 : ",voltage)
print("溫度 : ",temperature)

ser.close()