import cv2
import numpy as np
from pythonosc import udp_client

# 打开摄像头
cap = cv2.VideoCapture(0)

# OSC客户端设置
osc_client = udp_client.SimpleUDPClient("127.0.0.1", 5005)  # OSC接收器的IP和端口

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开摄像头，请检查代码中的摄像头索引。")
    exit()

while True:
    # 读取摄像头图像
    ret, frame = cap.read()

    # 检查帧是否成功捕获
    if not ret:
        print("无法从摄像头读取图像，请检查代码中的摄像头索引。")
        break

    # 将图像转换为HSV颜色空间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 定义黑色的颜色范围
    lower_black = np.array([0, 0, 200])
    upper_black = np.array([180, 30, 255])

    # 创建掩码
    mask = cv2.inRange(hsv, lower_black, upper_black)

    # 查找轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 如果找到轮廓，则处理最大轮廓
    if contours:
        max_contour = max(contours, key=cv2.contourArea)

        # 计算轮廓的边界矩形
        x, y, w, h = cv2.boundingRect(max_contour)

        # 绘制矩形框选识别到的物体
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 计算轮廓的中心坐标
        M = cv2.moments(max_contour)
        if M["m00"] != 0:
            center_x = int(M["m10"] / M["m00"])
            center_y = int(M["m01"] / M["m00"])

            # 在图像上绘制小球的中心
            cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)

            # 在控制台输出小球的坐标
            print(f"球的坐标：({center_x}, {center_y})")

            # 通过OSC发送小球的坐标
            osc_client.send_message("/ball/position", [center_x, center_y])

    # 显示图像
    cv2.imshow("Frame", frame)

    # 检测键盘按键，如果按下'q'键，则退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 关闭摄像头和窗口
cap.release()
cv2.destroyAllWindows()
