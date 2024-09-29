import time
import serial
import struct

# 配置串行通訊參數
ser = serial.Serial(
    port='COM14',  # 這裡的端口號根據您的設備而定
    baudrate=115200,        # 設置波特率
    parity='E',
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1             # 讀取超時設置
)
def calculate_crc(data):
    # 计算CRC的函数，此处需要实现CRC-16/MODBUS的计算
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for i in range(8):
            if (crc & 1) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return struct.pack('<H', crc)  # 返回低字节在前的CRC值

# 發送數據
# ser.write( bytes([0x01, 0x06, 0x00, 0x10, 0x00, 0x90, 0x88, 0x63]))  # Start Num0 PDF.54 Chacter 7.3.2.1
# ser.write( bytes([0x01, 0x06, 0x00, 0x10, 0x00, 0x91, 0x49, 0xA3]))  # Start Num1
#CRC校驗碼需隨前面的Byte數做調整
setup_parameter = bytes([0x01, 0x10,
                  0x12,0x00,
                  0x00,0x03,#3個字 1Word = 2bytes
                  0x06,#6 bytes
                  0x01,0xF4, #夾爪開度 0~1000 = 0~100% 0x01F4 = 500
                  0x03,0xE8, #設定移動速度
                  0x03,0x20, #設定爪力 0~1000 = 0~100% 0x02EE = 750
                  # 0x08,0xA0 #CRC
                  ])
setup_parameter += calculate_crc(setup_parameter)
ser.write(setup_parameter)  # SetUP Num2
#

received_data = ser.readline()  
print(received_data)
# time.sleep(1)


"""Num1"""
ser.write( bytes([0x01, 0x06, 0x00, 0x10, 0x00, 0x91, 0x49, 0xA3]))  # Start Num1
time.sleep(1)
# 接收數據 Num1
received_data = ser.readline()  # 讀取10個字節的數據
print(received_data)
time.sleep(1)

"""Num0"""
ser.write(bytes([0x01, 0x06, 0x00, 0x10, 0x00, 0x90, 0x88, 0x63]))  # Start Num0

# 接收數據 Num0
received_data = ser.readline()  
print("Number : ",received_data)

"""Num2"""
# ser.write( bytes([0x01, 0x06, 0x00, 0x10, 0x00, 0x92, 0x09, 0xA2]))  # Start Num1
# time.sleep(1)
# # 接收數據 Num1
# received_data = ser.readline()  # 讀取10個字節的數據
# print(received_data)
# 關閉串行通訊

ser.close()

print(received_data)