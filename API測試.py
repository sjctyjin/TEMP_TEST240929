import requests

hostIP = "192.168.2.105"

url = f'http://{hostIP}:8081/RoboControl.aspx/Web_SetCoords'

# if data_res['classname'] == "Kumquat_mature":
#     on_grap = 1  # RO[4] = ON
# else:
on_grap = 1  # RO[4] = OFF
posex = 612.5
posey = -191
posez = 212.5
# 準備要發送的數據，這裡假設您要傳遞一個JSON對象
data = {'cordX': posex, 'cordY': posey, 'cordZ': posez, 'cordW': "", 'cordP': "", 'cordR': "", 'ONGRAP': on_grap}

# 使用requests庫發送POST請求
response = requests.post(url, json=data, verify=False)

# 檢查請求是否成功
if response.status_code == 200:
    print('POST請求成功')
    print('伺服器回應：', response.text)
    RDO1 = 1
    while RDO1:
        data = {"data": "get"}
        url = f'http://{hostIP}:8081/RoboControl.aspx/Web_ReadRDO'
        # 使用requests庫發送POST請求
        response = requests.post(url, json=data, verify=False)
        # 檢查請求是否成功
        if response.status_code == 200:

            print('伺服器回應：', response.json()["d"])

            if response.json()["d"] == "1":
                print("抓取")
                ser = serial.Serial(
                        port='/dev/ttyUSB0',  # 這裡的端口號根據您的設備而定
                        baudrate=115200,  # 設置波特率
                        parity='E',
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=1  # 讀取超時設置
                    )
                """Num1"""
                ser.write(bytes([0x01, 0x06, 0x00, 0x10, 0x00, 0x91, 0x49, 0xA3]))  # Start Num1
                time.sleep(1)
                # 接收數據 Num1
                received_data = ser.readline()  # 讀取10個字節的數據
                print(received_data)
                time.sleep(1)
                break
        else:
            print('POST請求失敗')
        time.sleep(1)
    labels_api = []
    # ser = serial.Serial(
    #     port='/dev/ttyUSB0',  # 這裡的端口號根據您的設備而定
    #     baudrate=115200,  # 設置波特率
    #     parity='E',
    #     stopbits=serial.STOPBITS_ONE,
    #     bytesize=serial.EIGHTBITS,
    #     timeout=1  # 讀取超時設置
    # )
    # """Num0"""
    # ser.write(bytes([0x01, 0x06, 0x00, 0x10, 0x00, 0x90, 0x88, 0x63]))  # Start Num0
    #
    # # 接收數據 Num0
    # received_data = ser.readline()  # 讀取10個字節的數據
    # print(received_data)
    # ser.close()
else:
    print('POST請求失敗')
