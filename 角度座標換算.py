import math
import matplotlib.pyplot as plt

a, b = 210, 0   # 圆心坐标

w = 540  # 将圆平均分为 100 份
m = (2 * math.pi)       # 每一份对应的弧度

r = 540  # 半径

x_list = [210]
y_list = [0]

for i in [0,90,180,-90]:
    x = a + r * math.sin(m * (i/360))
    y = b + r * math.cos(m * (i/360))
    x_list.append(x)
    y_list.append(y)

# 绘制图形
plt.figure()
plt.plot(x_list, y_list, 'o-', label='圆周上的点')
plt.xlabel('X 轴')
plt.ylabel('Y 轴')
plt.title('圆的绘制（100 等分）')
plt.legend()
plt.grid(True)
plt.axis('equal')  # 保持 X 和 Y 轴比例一致
plt.show()
#
# import struct
# send_pos =[0x01,0xfd,0x04,0x01,0x00,0x00,0x00,0x00,0x6B]
# print(bytes(send_pos))
# send_pos[6:8] = struct.pack('h', 16000)
# # send_pos[6] = struct.pack('h', 16000)[0]
# # send_pos[7] = struct.pack('h', 16000)[1]
# print(struct.pack('>h', 14))
# print(bytes(send_pos))
