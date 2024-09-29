import time
import struct
import serial

def calculate_crc(data):
    # 簡單的累加和取反
    crc = sum(data) & 0xFF  # 累加和取低 8 位
    return crc

try:
    # 初始化串口
    ser = serial.Serial('COM14', 38400, timeout=0.1)

    # 要發送的指令，例如：FA 01 F6 01
    # command = bytearray([0xFA, 0x01, 0xF6, 0x01])
    # command = bytearray([0xFA, 0x01, 0xF3, 0x00,0xEE])
    # FB 01 30 FF FF FF FF 3D C3 28
    # FA
    # 01
    # FD
    # 02
    # 00
    # 00
    # 0
    # C
    # 80
    # command = bytearray([0xFA, 0x01, 0xF7])
    # command = [0xFA,0x01,0x86]
    # 2. 电机以速度100RPM，加速度2，正转一圈（3200脉冲）
    # 发送指令：FA 01 FD 80 64 02 00 00 0C 80 6A
    # 頭文、addr、功能碼(位置控制模式)、馬達反轉、速度、加速度、脉冲数(4bytes)、CRC校驗位(字串總數)
    #不始能
    # command = [0xFA,0x01,0xF3,0x00]
    #始能
    command = [0xFA,0x01,0xF3,0x01]
    speed = 0x02#100
    #馬達反轉含轉速及pluse，脈衝值為正
    command = [0xFA,0x01,0xFD,0x00,speed,0x10,0x00,0x00,0x06,0x40] #送衝1600脈衝
    # #馬達正轉含轉速及pluse，脈衝值為負
    # command = [0xFA,0x01,0xFD,0x00,speed,0x10,0x00,0x00,0x06,0x40]
    # command = bytearray([0xFA, 0x01, 0x30])
    # FA 01 FD 01 00 00 0C 80 85
    # command = [0xFA, 0x01, 0xFD, 0x01, 0x00,0x00, 0x0C, 0x80,0x85]
    # FA 01 83 06 84
    # 計算CRC並附加到指令後面
    crc = calculate_crc(command)
    command.append(crc)
    print(command)
    # 發送指令
    ser.write(bytes(command))
    time.sleep(1)
    #清空接收緩衝區
    ser.readall()
    #讀取當前脈衝值
    command = [0xFA,0x01,0x33]
    # 計算CRC並附加到指令後面
    crc = calculate_crc(command)
    command.append(crc)
    # 發送指令
    ser.write(bytes(command))
    data = ser.readall()
    print(data)
    print(data[3:7])
    print(f"Sent command: {struct.unpack('>i',data[3:7])[0]}")
except:
    pass

# FF FF F9 C0
# def calculate_crc(data):
#     crc = 0
#     for byte in data:
#         crc += byte
#     crc = ~crc & 0xFF  # 取反並保留低8位
#     return crc
#
# # 指令數據
command = bytearray([0xFA, 0x01, 0xF3, 0x00])
command = bytearray([0xFB, 0x01, 0x33, 0xFF, 0xFF, 0xF9,0xC0])
command = bytearray([0xFA,0x01,0xFD,0x80,0x01,0x1E,0x00,0x00,0x06,0x40])
# FB 01 33 FF FF F9 C0
# 計算 CRC
crc = calculate_crc(command)
print(f"CRC: {hex(crc)}")

def calculate_crc(data):
    crc = sum(data) & 0xFF  # 累加和取低 8 位
    return crc

# 指令數據
# command = bytearray([0xFA, 0x01, 0xF3, 0x00])
# command = bytearray([0xFA, 0x01, 0xFD, 0x80, 0xC8, 0x10, 0x00, 0x00, 0x00, 0xC8])
# FA 01 FD 02 00 00 0C 80
# 計算 CRC
# crc = calculate_crc(command)
# print(f"CRC: {hex(crc)}")
