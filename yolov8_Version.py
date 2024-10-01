import time
import cv2
import numpy as np
import pyrealsense2 as rs
from PIL import Image
import serial
from ultralytics import YOLO  # 将YOLOv8导入到该py文件中
# import torch
#
# print(torcu.cuda.is_available())
''' 深度相机 '''
pipeline = rs.pipeline()  # 定义流程pipeline，创建一个管道
config = rs.config()  # 定义配置config

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)  # 配置depth流
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)  # 配置color流

pipe_profile = pipeline.start(config)  # streaming流开始
align = rs.align(rs.stream.color)

"""
Arduino
"""
port = 'COM7'  # 根据您的情况更改端口号，例如在Windows上可能是 'COM3'
baudrate = 115200  # 波特率需要与Arduino上的设置一致
Arduino = serial.Serial(port, baudrate, timeout=0.2)

def GET_POS(ser2):
    global height_limit
    previous_line = ""
    time.sleep(1)  # 等待Arduino响应
    ser2.write(b'GETPOS\n')  # 发送'hello'指令
    time.sleep(0.2)  # 等待Arduino响应
    while True:
        # 從串口讀取一行數據
        current_line = ser2.readline().decode().strip()

        if current_line:
            # print(f"Current Line: {current_line}")
            # 如果讀取到 "Done"，則回溯上一段字串
            if current_line == "DONE":
                # print(f"Previous Line before 'Done': {previous_line}")
                break
            # 更新 previous_line 為當前讀取的數據
            previous_line = current_line

        else:
            break
    return previous_line
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
        # print("發送移動指令")
        ser2.write(bytes(f"{sx},{sy},{sz},{sw}\n".encode()))  # 发送'hello'指令
        time.sleep(1)
    start_time = time.time()
    while True:
        if ser2.in_waiting > 0:
            response = ser2.readline().decode().strip()
            # print("Arduino:", response)
            if response == "DONE":
                break
        if time.time() - start_time > 30:
            print("Timeout waiting for Arduino.")
            break
        time.sleep(1)

def get_aligned_images():
    frames = pipeline.wait_for_frames()  # 等待获取图像帧，获取颜色和深度的框架集
    aligned_frames = align.process(frames)  # 获取对齐帧，将深度框与颜色框对齐

    aligned_depth_frame = aligned_frames.get_depth_frame()  # 获取对齐帧中的的depth帧
    aligned_color_frame = aligned_frames.get_color_frame()  # 获取对齐帧中的的color帧

    #### 获取相机参数 ####
    depth_intrin = aligned_depth_frame.profile.as_video_stream_profile().intrinsics  # 获取深度参数（像素坐标系转相机坐标系会用到）
    color_intrin = aligned_color_frame.profile.as_video_stream_profile().intrinsics  # 获取相机内参

    img_color = np.asanyarray(aligned_color_frame.get_data())  # RGB图
    img_depth = np.asanyarray(aligned_depth_frame.get_data())  # 深度图（默认16位）

    depth_colormap = cv2.applyColorMap \
        (cv2.convertScaleAbs(img_depth, alpha=0.008)
         , cv2.COLORMAP_JET)

    return depth_intrin, img_color, aligned_depth_frame

def calculate_new_base_position(current_base_pos, target_camera_coords):
    x_base, y_base, z_base = current_base_pos
    x_cam, y_cam, z_cam = target_camera_coords
    pos = 0
    # 計算新基座位置
    if pos == 3:
        x_new = x_base + (x_cam) - 20
    x_new = x_base - (x_cam) + 20
    y_new = y_base - z_cam
    z_new = z_base - (y_cam) + 60

    return (x_new, y_new, z_new)

if __name__ == '__main__':
    model = YOLO(r"D:\技術文件\Python專案\ultralytics\yolov8n.pt")  # 加载权重文件，如需要更换为自己训练好的权重best.pt即可
    set_move = -1  # 初始位移状态
    # 设置计时器
    start_time = time.time()
    interval = 0.01  # 间隔时间（秒）
    try:
        while True:
            depth_intrin, img_color, aligned_depth_frame = get_aligned_images()  # 获取对齐图像与相机参数
            # 检查是否达到间隔时间
            if time.time() - start_time >= interval:
                start_time = time.time()  # 重置计时器
                # source = [img_color]
                source = img_color
                # 调用YOLOv8中的推理，还是相当于把d435i中某一帧的图片进行detect推理
                results = model.predict(source, save=False, show_conf=False)

                for result in results:  # 相当于都预测完了才进行的打印目标框，这样就慢了
                    boxes = result.boxes.xywh.tolist()
                    tags = result.names  # 获取标签
                    # im_array = result.plot()  # plot a BGR numpy array of predictions
                    im_array = source # plot a BGR numpy array of predictions

                    for i in range(len(boxes)):
                        if tags[result.boxes[i].cls[0].item()]  == 'cup':  # 筛选出杯子

                            print(result.boxes[i].cls[0].item())
                            ux, uy = int(boxes[i][0]), int(boxes[i][1])  # 计算像素坐标系的x
                            dis = aligned_depth_frame.get_distance(ux, uy)
                            camera_xyz = rs.rs2_deproject_pixel_to_point(depth_intrin, (ux, uy), dis)  # 计算相机坐标系的xyz
                            # diplace_move = rs.rs2_deproject_pixel_to_point(depth_intrin, (ux+66, uy+140), dis)  # 计算相机坐标系的xyz
                            camera_xyz = np.round(np.array(camera_xyz), 3)  # 转成3位小数
                            # diplace_move = np.round(np.array(diplace_move), 3)  # 转成3位小数
                            camera_xyz = np.array(list(camera_xyz)) * 1000
                            # diplace_move = np.array(list(diplace_move)) * 1000
                            camera_xyz = list(camera_xyz)
                            # print("X :",[diplace_move][0][0])
                            # print("Y :",[diplace_move][0][1])

                            cv2.circle(im_array, (ux, uy), 4, (255, 255, 255), 5)  # 标出中心点
                            cv2.putText(im_array, str(camera_xyz), (ux + 20, uy + 10), 0, 0.5,
                                        [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)  # 标出坐标
                            """
                            # 位移
                            """
                            if set_move == 1:
                                data = GET_POS(Arduino)
                                print(data)
                                x = float(data.split(',')[0].split(':')[1])
                                y = float(data.split(',')[1].split(':')[1])
                                z = float(data.split(',')[2].split(':')[1])
                                current_base_pos = (x, y, z)
                                target_camera_coords = (camera_xyz[0], camera_xyz[1], camera_xyz[2])
                                # target_camera_coords2 = ([diplace_move][0][0], [diplace_move][0][1], camera_xyz[2])
                                new_base_pos = calculate_new_base_position(current_base_pos, target_camera_coords)
                                # new_base_pos2 = calculate_new_base_position(current_base_pos, target_camera_coords2)

                                print(f"原始座標: {current_base_pos}")
                                print(f"相機座標: {target_camera_coords}")
                                print(f"新的基座目標位置X: {new_base_pos[0]}")
                                print(f"新的基座目標位置Z: {new_base_pos[2]}")
                                set_move = 0
                                Axis_move(Arduino, new_base_pos[0], y, new_base_pos[2], 0)
                                # time.sleep(5)
                            # print(f"新的基座目標位置(位移): {new_base_pos2}")
                cv2.circle(im_array, (im_array.shape[1]//2, im_array.shape[0]//2), 5, (0, 0, 255), 5)  # 标出中心点
                cv2.circle(im_array, (im_array.shape[1]//2+66, im_array.shape[0]//2+140), 1, (0, 0, 255), 1)  # 标出中心点
                cv2.namedWindow('detection', flags=cv2.WINDOW_NORMAL |
                                                   cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED)
                cv2.resizeWindow('detection', 640, 480)
                cv2.imshow('detection', im_array)
                # cv2.waitKey(0)

            key = cv2.waitKey(1)
            # Press esc or 'q' to close the image window
            if key == 27 or key == ord('k'):
                set_move = 1
            if key & 0xFF == ord('q') or key == 27:
                cv2.destroyAllWindows()
                pipeline.stop()
                break
    finally:
        # Stop streaming
        pipeline.stop()