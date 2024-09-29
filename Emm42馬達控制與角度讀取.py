import serial
import time
import struct
import math
# 设置串口参数
set_pos = -1      #旋轉姿態 4 種
height_limit = 1 #高度限制開關
#歸零指令
def zero_angle(ser):
    ser.write(b'\x01\x33\x6B')
    data = ser.readall()
    if struct.unpack('>I', data[1:-1])[0] > 65536:
        current_angel = struct.unpack('>I', data[1:-1])[0] - (65536 ** 2)
        degree = current_angel // 44.4

        # print((struct.unpack('>I', data[1:-1])[0] - (65536 ** 2)))
        # print((struct.unpack('>I', data[1:-1])[0] - (65536 ** 2)) // 44.4)
    else:
        current_angel = struct.unpack('>I', data[1:-1])[0]
        degree = current_angel // 44.4
        # print((struct.unpack('>I', data[1:-1])[0]))
        # print((struct.unpack('>I', data[1:-1])[0]) // 44.4)

    print("歸零 : " , current_angel)
    print("角度 : " , degree)
    if degree < 0:
    # 发送指令
    #     ser.write(b'\x01\xfd\x14\xff\x00\x00\x00\x00\x6B')
        send_pos = [0x01, 0xfd, 0x10, 0x1C, 0x00, 0x00, 0x00, 0x00, 0x6B]
        send_pos[4:8] = struct.pack('>I', abs(current_angel))
        print("小於0 : ",send_pos)
        print("小於0 : ",bytes(send_pos))
        ser.write(bytes(send_pos))
    else:
        send_pos = [0x01,0xfd,0x00,0x1C,0x00,0x00,0x00,0x00,0x6B]
        send_pos[4:8] = struct.pack('>I', abs(current_angel))
        print("大於0 : ",send_pos)
        ser.write(bytes(send_pos))
    time.sleep(2)  # 等待Arduino响应
#設定旋轉四位置
def set_degress(ser,mode):
    global height_limit
    global set_pos
    # 0: 原點 1: 右邊 2: 後面 3: 左邊
    ser.readall()
    degree_list = [0,90,180,-90]
    ser.write(b'\x01\x33\x6B')
    data = ser.readall()
    print("初始角度 : ",data)
    if struct.unpack('>I', data[1:-1])[0] > 65536:
        current_angel = struct.unpack('>I', data[1:-1])[0] - (65536 ** 2)
        degree = current_angel // 44.4
    else:
        current_angel = struct.unpack('>I', data[1:-1])[0]
        degree = current_angel // 44.4

    time.sleep(0.1)

    ser.write(b'\x01\x36\x6B')
    data = ser.readall()
    decode_degree = struct.unpack('>I', data[1:-1])[0]

    if decode_degree > 65536 * 10:
        print(decode_degree - 65536 ** 2)
        current_degree = ((decode_degree - 65536 ** 2) * 360) / 65536
        print("角度負值 : ", current_degree // 5)
    else:
        current_degree = ((decode_degree * 360)) / 65536
        print("角度 : ", current_degree // 5)
    #高度限制確認
    if height_limit == 1:
        print("高度限制，無法設定")
        return
    # if set_pos == 2 or mode == 0:
    #     if height_limit == 1:
    #         print("高度限制，無法設定")
    #         return
    # elif mode == 2:
    #     if height_limit == 1:
    #         print("高度限制，無法設定")
    #         return
    #模式選擇
    speed = 0x32#速度設定
    Foward = 0x10   # 正反轉(逆時針)
    Backward = 0x00 # 正反轉(順時針)
    cudeg = current_degree // 5 * -1

    if mode == 0:
        print("歸零----------")
        zero_angle(ser)
    elif mode == 1:
        # -90度以下 情況
        if cudeg < 0:
            print("角度脈衝值 : ",current_angel)
            send_pos = [0x01, 0xfd, Backward, speed, 0x00, 0x00, 0x00, 0x00, 0x6B]
            send_pos[6:8] = struct.pack('>h', abs(current_angel  + int(degree_list[mode]*44.4)))
            print("移動到右邊-小於0 : ", send_pos)
            print("小於0 : ", bytes(send_pos))
            # ser.write(bytes(send_pos))
        # 90度以上 情況
        elif cudeg > 90:
            print("角度脈衝值 : ", current_angel)
            send_pos = [0x01, 0xfd, Foward, speed, 0x00, 0x00, 0x00, 0x00, 0x6B]
            print("移動到右邊-大於90 : ",current_angel + (degree_list[mode]*44.4))
            send_pos[6:8] = struct.pack('>h', abs(current_angel + int(degree_list[mode]*44.4)))
            ser.write(bytes(send_pos))
            print("移動到右邊-大於90 : ", send_pos)
        # 0~90度 情況
        else:
            print("角度脈衝值 : ",current_angel)
            send_pos = [0x01, 0xfd, Backward, speed, 0x00, 0x00, 0x00, 0x00, 0x6B]
            print("移動到右邊-0~90 : ", (degree_list[mode] ))
            send_pos[6:8] = struct.pack('>h', abs(current_angel+int(degree_list[mode]*44.4)))
            print("移動到右邊-0~90 : ", send_pos)
            ser.write(bytes(send_pos))
        # send_pos = [0x01, 0xfd, 0x10, 0x32, 0x00, 0x00, 0x00, 0x00, 0x6B]
        # send_pos[6:8] = struct.pack('>h', degree[mode])
        # ser.write(bytes(send_pos))
    elif mode == 2:
        if cudeg < 0:
            send_pos = [0x01, 0xfd, Backward, speed, 0x00, 0x00, 0x00, 0x00, 0x6B]
            send_pos[6:8] = struct.pack('>h', abs(current_angel + int(degree_list[mode] * 44.4)))
            print("移動到後面-小於0 : ", send_pos)
            # print("小於0 : ", bytes(send_pos))
            ser.write(bytes(send_pos))
        # 90度以上 情況
        elif cudeg > 90:
            print("角度脈衝值 : ", current_angel)
            send_pos = [0x01, 0xfd, Backward, speed, 0x00, 0x00, 0x00, 0x00, 0x6B]
            send_pos[6:8] = struct.pack('>h', abs(current_angel + int(degree_list[mode] * 44.4)))
            print("移動到後面-等於180 : ", send_pos)
            ser.write(bytes(send_pos))
        # 0~90度 情況
        else:
            print("角度脈衝值 : ",current_angel)
            send_pos = [0x01, 0xfd,Backward, speed, 0x00, 0x00, 0x00, 0x00, 0x6B]
            send_pos[6:8] = struct.pack('>h', abs(current_angel + int(degree_list[mode] * 44.4)))
            print("移動到後面-0~90 : ", send_pos)
            ser.write(bytes(send_pos))
    elif mode == 3:
        print("當前脈衝數 : ",current_angel)
        print("當前脈角度 : ",cudeg)
        if cudeg < 0:
            print("脈衝設定值 : ",abs(current_angel + int(degree_list[mode] * 44.4)))
            send_pos = [0x01, 0xfd, Backward, speed, 0x00, 0x00, 0x00, 0x00, 0x6B]
            send_pos[6:8] = struct.pack('>h', abs(current_angel + int(degree_list[mode] * 44.4)))
            print("移動到左邊-小於0 : ", send_pos)
            # print("小於0 : ", bytes(send_pos))
            ser.write(bytes(send_pos))
        else:
            send_pos = [0x01, 0xfd, Foward, speed, 0x00, 0x00, 0x00, 0x00, 0x6B]
            send_pos[6:8] = struct.pack('>h', abs(current_angel + int(degree_list[mode] * 44.4)))
            print("移動到左邊-0~180 : ", send_pos)
            ser.write(bytes(send_pos))
    elif mode == 4:#不使能
        ser.write(b'\x01\xf3\x00\x6B')  # 不始能狀態 #始能狀態 b'\x01\xf3\x01\x6B'
        ser.readall()
        print("不使能")
    elif mode == 5:#使能
        ser.write(b'\x01\xf3\x01\x6B')  # 始能狀態 #不始能狀態 b'\x01\xf3\x00\x6B'
        ser.readall()
        print("使能")

def rotate(x,y,z,pos=0):
    global set_pos
    port = 'COM16'  # 根据您的情况更改端口号，例如在Windows上可能是 'COM3'
    baudrate = 38400  # 波特率需要与Arduino上的设置一致
    ser = serial.Serial(port, baudrate, timeout=0.2)

    #配置1:5減速馬達的話
    #設置16000脈衝為一圈 = 3200 * 5
    #即1度為 16000 / 360 = 44.4

    # for i in range(3):
    # #     # 发送指令
    #     ser.write(b'\x01\xfd\x00\x32\x00\x00\x0F\x78\x6B')
    #     time.sleep(2)  # 等待Arduino响应
    # degree = [0,90,180,-90]


    if set_pos != pos:
        set_degress(ser, pos)
        time.sleep(2)  # 等待Arduino响应
        set_pos = pos
    # ser.write(b'\x01\x36\x6B')#讀取角度值
    # # ser.write(b'\x01\xf3\x01\x6B')#不始能狀態 #始能狀態 b'\x01\xf3\x01\x6B'
    # time.sleep(1)  # 等待Arduino响应
    # data = ser.readall()
    # print(data[1:5])
    # decode_degree =struct.unpack('>I',data[1:-1])[0]
    # print(decode_degree)
    # if decode_degree > 65536*10:
    #     print(decode_degree-65536**2)
    #     current_angel = ((decode_degree-65536**2) * 360) / 65536
    #     print("當前角度負值 : ",current_angel//5)
    # else:
    #     current_angel = ((decode_degree * 360)) / 65536
    #     print("角度 : ",current_angel//5)
    ser.readall()
    ser.write(b'\x01\x33\x6B')  # 讀取脈衝值
    time.sleep(1)  # 等待Arduino响应
    data = ser.readall()
    if struct.unpack('>I',data[1:-1])[0] > 65536:
        print((struct.unpack('>I',data[1:-1])[0]-(65536**2)))
        current_angel = struct.unpack('>I',data[1:-1])[0]-(65536**2)
        print((struct.unpack('>I',data[1:-1])[0]-(65536**2))//44.4)
    else:
        print((struct.unpack('>I',data[1:-1])[0]))
        print((struct.unpack('>I',data[1:-1])[0])//44.4)
        current_angel = struct.unpack('>I',data[1:-1])[0]


    degree = current_angel // 44.4 * -1
    print("當前脈衝角度",degree)
    # print((struct.unpack('>I',data[1:-1])[0]*360)/65536)

    a,b = x,y   #圆点坐标

    w = 10  # 圆平均分为10份
    m = (2*math.pi)/w #一个圆分成10份，每一份弧度为 m
    r = 540  #半径
    point_list = ""
    print("當前座標 : ",a,b)
    print("角度換算值 : ",degree)
    print("弧度換算值 : ",degree/360*(2*math.pi))
    print("角度SIN值 : ",math.sin(degree))
    print("角度COS值 : ",math.cos(degree))
    print("弧度SIN值 : ",math.sin((degree/360)*(2*math.pi)))
    print("弧度COS值 : ",math.cos((degree/360)*(2*math.pi)))
    x = a + r * math.cos((degree / 360) * (2 * math.pi))
    y = b + r * math.sin((degree/360)*(2*math.pi))
    point_list += " X : {}, Y :{},Z : {}".format(round(x,2),round(y,2),z)
    print(point_list)
    # 关闭串口
    ser.close()
def Axis_move(ser2,sx=0,sy=0,sz=0,sw=0):
    """

    maxX = 210.04
    maxY = 189.65
    maxZ = 277.24
    maxW = 359.99

    :return:
    """
    time.sleep(1)  # 等待Arduino响应
    # data = ser2.readall().decode()  #
    if sx != 0 or sy != 0 or sz != 0 or sw != 0:
        print("發送移動指令")
        ser2.write(bytes(f"{sx},{sy},{sz},{sw}\n".encode()))  # 发送'hello'指令
        time.sleep(1)
    start_time = time.time()
    while True:
        if ser2.in_waiting > 0:
            response = ser2.readline().decode().strip()
            print("Arduino:", response)
            if response == "DONE":
                break
        if time.time() - start_time > 30:
            print("Timeout waiting for Arduino.")
            break
        time.sleep(1)

def GET_POS(ser2):
    global height_limit
    previous_line = ""
    time.sleep(1)  # 等待Arduino响应
    ser2.write(b'GETPOS\n')  # 发送'hello'指令
    # data = ser2.readall().decode().strip()
    time.sleep(0.2)  # 等待Arduino响应
    while True:
        # 從串口讀取一行數據
        current_line = ser2.readline().decode().strip()

        if current_line:
            print(f"Current Line: {current_line}")

            # 如果讀取到 "Done"，則回溯上一段字串
            if current_line == "DONE":
                print(f"Previous Line before 'Done': {previous_line}")
                break
            # 更新 previous_line 為當前讀取的數據
            previous_line = current_line
        else:
            break
    return previous_line
    # if data != "":
    #     print("GETPOS : ",data)
    #     # ser2.close()
    #     return data
    # else:
    #     # ser2.close()
    #     return "no data"
def Zero_Pos(ser2):
    global height_limit
    port = 'COM16'  # 根据您的情况更改端口号，例如在Windows上可能是 'COM3'
    baudrate = 38400  # 波特率需要与Arduino上的设置一致
    ser = serial.Serial(port, baudrate, timeout=0.5)
    time.sleep(1)
    #查看高度是否正確
    data = GET_POS(ser2)
    if len(data) > 35:
        print("測試 : ", data)
    else:
        x = int(data.split(',')[0].split(':')[1].split('.')[0])
        y = int(data.split(',')[1].split(':')[1].split('.')[0])
        z = int(data.split(',')[2].split(':')[1].split('.')[0])
    if z > 275:
        print("解除高度限制")
        height_limit = 0
    else:
        print("設定高度限制失敗")
        height_limit = 1

    try:
        set_degress(ser, 1)
    except:
        print("wrong")
        ser.close()
        return "wrong"
    time.sleep(1)  # 等待Arduino响应
    if height_limit == 0:
        ser2.write(b'zero\n')  # 发送'hello'指令
    ser.close()

def Max_Pos(ser2):
    global height_limit
    port = 'COM16'  # 根据您的情况更改端口号，例如在Windows上可能是 'COM3'
    baudrate = 38400  # 波特率需要与Arduino上的设置一致
    ser = serial.Serial(port, baudrate, timeout=0.2)
    ser.readall()
    degree_list = [0, 90, 180, -90]
    ser.write(b'\x01\x33\x6B')
    data = ser.readall()
    print("初始角度 : ", data)
    if struct.unpack('>I', data[1:-1])[0] > 65536:
        current_angel = struct.unpack('>I', data[1:-1])[0] - (65536 ** 2)
        degree = current_angel // 44.4
    else:
        current_angel = struct.unpack('>I', data[1:-1])[0]
        degree = current_angel // 44.4
    print("初始角度 : ", degree)
    ser.close()
    # time.sleep(1)  # 等待Arduino响应
    if degree in [-90, 90, -91, 91,89,-89]:
        ser2.write(b'max\n')  # 发送'hello'指令

def ZMAX(ser2):
    global height_limit
    ser2.write(b'StepperZ+ 10000\n')  # 发送'hello'指令
    # ser.close()
# Axis_move(0,180,200,0)
# time.sleep(2)
# data = GET_POS()
# if len(data) > 35:
#     print("測試 : ",data)
# else:
#     x = int(data.split(',')[0].split(':')[1].split('.')[0])
#     y = int(data.split(',')[1].split(':')[1].split('.')[0])
#     z = int(data.split(',')[2].split(':')[1].split('.')[0])
#
#     print(x,y,z)
#     """
#     mode = 0 # 0:歸零 1:右邊 2:後面 3:左邊 4:不使能 5:使能
#     """
#     rotate(x,y,z,1)
#     print(set_pos)
def Setting_End_Effector(ser2,efx,efy,efz,efw=0):
    global height_limit
    data = GET_POS(ser2)
    if len(data) > 35:
        print("測試 : ", data)
    else:
        x = int(data.split(',')[0].split(':')[1].split('.')[0])
        y = int(data.split(',')[1].split(':')[1].split('.')[0])
        z = int(data.split(',')[2].split(':')[1].split('.')[0])
    if z > 255:
        print("解除高度限制")
        height_limit = 0
    else:
        print("設定高度限制失敗")
        height_limit = 1
    print("高度限制 ~~: ",height_limit)
    #當mode = 1，右邊時，座標移動方式為Axis_move(efx, 540+efy, efz, 0)
    #當mode = 3，左邊時，座標移動方式為Axis_move(efx, efy-540, efz, 0)
    #當mode = 2，後面時，座標移動方式為X一定為負數
    print(efx, y+efy, z)
    Axis_move(ser2,efx, 540+efy, efz, 30)
    time.sleep(2)
    data = GET_POS(ser2)
    print(data)
    # if len(data) < 35:
    #     x = int(data.split(',')[0].split(':')[1].split('.')[0])
    #     y = int(data.split(',')[1].split(':')[1].split('.')[0])
    #     z = int(data.split(',')[2].split(':')[1].split('.')[0])
    #     port = 'COM16'  # 根据您的情况更改端口号，例如在Windows上可能是 'COM3'
    #     baudrate = 38400  # 波特率需要与Arduino上的设置一致
    #     ser = serial.Serial(port, baudrate, timeout=0.2)
    #     ser.readall()
    #     ser.write(b'\x01\x33\x6B')  # 讀取脈衝值
    #     time.sleep(1)  # 等待Arduino响应
    #     data = ser.readall()
    #     if struct.unpack('>I', data[1:-1])[0] > 65536:
    #         print((struct.unpack('>I', data[1:-1])[0] - (65536 ** 2)))
    #         current_angel = struct.unpack('>I', data[1:-1])[0] - (65536 ** 2)
    #         print((struct.unpack('>I', data[1:-1])[0] - (65536 ** 2)) // 44.4)
    #     else:
    #         print((struct.unpack('>I', data[1:-1])[0]))
    #         print((struct.unpack('>I', data[1:-1])[0]) // 44.4)
    #         current_angel = struct.unpack('>I', data[1:-1])[0]
    #     degree = current_angel // 44.4 * -1
    #     print("當前脈衝角度", degree)
    #     a, b = x, y  # 圆点坐标
    #     r = 540  # 半径
    #     point_list = ""
    #     print("當前座標 : ", efx, b)
    #     # print("角度換算值 : ", degree)
    #     # print("弧度換算值 : ", degree / 360 * (2 * math.pi))
    #     # print("角度SIN值 : ", math.sin(degree))
    #     # print("角度COS值 : ", math.cos(degree))
    #     # print("弧度SIN值 : ", math.sin((degree / 360) * (2 * math.pi)))
    #     # print("弧度COS值 : ", math.cos((degree / 360) * (2 * math.pi)))
    #     x = a + r * math.cos((degree / 360) * (2 * math.pi))
    #     y = b + r * math.sin((degree / 360) * (2 * math.pi))
    #     point_list += " X : {}, Y :{},Z : {}".format(round(x, 2), round(y, 2), z)
    #     print("末端坐標 : ",point_list)
    #     # 关闭串口
    #     ser.close()
    #     ser2.close()

port = 'COM7'  # 根据您的情况更改端口号，例如在Windows上可能是 'COM3'
baudrate = 115200  # 波特率需要与Arduino上的设置一致
ser2 = serial.Serial(port, baudrate, timeout=0.2)

# Max_Pos(ser2)
# Setting_End_Effector(ser2,150, -540, 250)
# time.sleep(1)
# Setting_End_Effector(ser2,150, -540, 250,180)
# time.sleep(1)
# Setting_End_Effector(ser2,150, -540, 250,180)
# time.sleep(1)
# Setting_End_Effector(ser2,150, -540, 270,180)
# time.sleep(1)
# print("高度限制 : ",height_limit)
# height_limit = 0
#======================================================
port = 'COM16'  # 根据您的情况更改端口号，例如在Windows上可能是 'COM3'
baudrate = 38400  # 波特率需要与Arduino上的设置一致
ser = serial.Serial(port, baudrate, timeout=0.2)
ser.readall()
degree_list = [0,90,180,-90]
ser.write(b'\x01\x33\x6B')
data = ser.readall()
print("初始角度 : ",data)
if struct.unpack('>I', data[1:-1])[0] > 65536:
    current_angel = struct.unpack('>I', data[1:-1])[0] - (65536 ** 2)
    degree = current_angel // 44.4
else:
    current_angel = struct.unpack('>I', data[1:-1])[0]
    degree = current_angel // 44.4
print("初始角度 : ",degree)
ser.close()

# ser2 = serial.Serial(port, baudrate, timeout=0.5)
time.sleep(1)
# rotate(150,-540,270,pos=0)
# data = GET_POS(ser2)
# print(data)
# Max_Pos(ser2)
# ZMAX(ser2)
# Zero_Pos_Rotate(ser2)
# Axis_move(ser2,0, 0, 0, -180)

# Zero_Pos(ser2)
# pos = 1
# if set_pos != pos:
#
height_limit = 0
rotate(150,-540,270,pos=1)
