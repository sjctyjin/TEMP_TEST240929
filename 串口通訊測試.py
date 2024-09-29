import serial
import time
import struct
# 设置串口参数
port = 'COM13'  # 根据您的情况更改端口号，例如在Windows上可能是 'COM3'
baudrate = 115200        # 波特率需要与Arduino上的设置一致

# 初始化串口连接
ser = serial.Serial(port, baudrate, timeout=0.2)
# time.sleep(1)  # 等待Arduino复位和初始化
# print(ser.readall().decode())  #
# ser.readall()  # 清空缓冲区
# time.sleep(1)  # 等待Arduino复位和初始化

# 发送指令
# ser.write(b'\x01\x36\x6B')
# # time.sleep(1)  # 等待Arduino响应
# data = ser.readall()
# print(data[1:])
ser.write(b'\x01\x36\x6B')#讀取角度
data = ser.readall()
current_angel = struct.unpack('>I', data[3:7])[0]
degree = round(((current_angel*360)/65536) / 5,1)
if data[2] == 1:
    degree = degree * -1

print("歸零 : " , (current_angel*360)/65535)
print("歸零 : " , current_angel)
print("角度 : " , degree)

#================================================================================

# 发送 讀取 設定值 指令
# ser.write(b'\x01\x33\x6B')
# # time.sleep(1)  # 等待Arduino响应
#================================================================================
# ser.write(b'\x01\x33\x6B')
# data = ser.readall()
# print(data)
# print(data[0])
# print(data[1])
# print(data[2])
# print(data[3])
# print(data[4])
# print(data[5])
# print(data[6])
# print(data[7])
# print(data[3:7])
#
# current_angel = struct.unpack('>I', data[3:7])[0]
# degree = current_angel // 44.4
#     # print((struct.unpack('>I', data[1:-1])[0]))
#     # print((struct.unpack('>I', data[1:-1])[0]) // 44.4)
#
# print("歸零 : " , (current_angel*360)/65536)
# print("歸零 : " , current_angel)
# print("角度 : " , degree)

#================================================================================

ser.write(b'\x01\x32\x6B')#讀取脈衝
data = ser.readall()
current_angel = struct.unpack('>I', data[3:7])[0]
degree = current_angel // 44.4
if data[2] == 1:
    degree = degree * -1

print("歸零 : " , (current_angel)/44.4)
print("脈衝 : " , current_angel)
print("角度 : " , degree)

#始能
# 01 F3 AB 01 00 6B
# ser.write(b'\x01\xf3\xab\01\00\x6B')
#不使能
#01 F3 AB 00 00 6
# ser.write(b'\x01\xf3\xab\00\00\x6B')
#角度清零
#01 0A 6D 6B
# ser.write(b'\x01\x0A\x6D\x6B')

#位置控制
"""
命令格式：地址 + 0xFD + 方向 + 速度+ 加速度 + 脉冲数 + 相对/绝对模式标志 + 多机同步标志 + 校验字节

        命令返回：地址 + 0xFD + 命令状态 + 校验字节
"""
#01 FD 01 05 DC 00 00 00 7D 00 00 00 6B
# ser.write(b'\x01\xfd\x01\x00\x64\x00\x00\x00\x0C\x80\x00\x00\x6B')
# ser.write(b'\x01\xfd\x01\x00\x64\x00\x00\x00\x06\x40\x00\x00\x6B')
# time.sleep(1)
ser.write(b'\x01\xfd\x00\x00\x64\x1E\x00\x00\x0C\x80\x00\x00\x6B')#180度
# ser.write(b'\x01\xfd\x00\x00\xC8\x00\x00\x00\x3E\x80\x00\x00\x6B')#16000脈衝 1800度圈
# 关闭串口
ser.close()
