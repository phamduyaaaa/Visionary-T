import pyautogui
import time
import os
import cv2
import numpy as np
#Vị trí hiện tại của chuột là: Point(x=186, y=188); Vị trí hiện tại của chuột là: Point(x=1145, y=973)
#Lấy vị trí hiện tại của chuột
# time.sleep(10)
# current_position = pyautogui.position()
# print(f'Vị trí hiện tại của chuột là: {current_position}')
time.sleep(5)
print("Start!!")
for i in range(300):
    for j in range(5):
        print(f"Screenshot after {4-j}s")
        time.sleep(1)
    print(f"Epoch: {i+1+500}")
    # Định nghĩa tọa độ và kích thước của vùng chụp
    # (x, y, width, height)
    # 1148 , 973
    region = (12, 180, 800, 800)   # Thay đổi tọa độ và kích thước theo ý bạn
    # Chụp màn hình vùng đã định nghĩa
    screenshot = pyautogui.screenshot(region=region)
    # Chuyển đổi ảnh từ PIL sang NumPy array
    screenshot = np.array(screenshot)

    # Chuyển đổi màu từ RGB sang BGR
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    # Chụp màn hình vùng đã định nghĩa

    # Đường dẫn lưu ảnh
    save_path = os.path.join('data', 'test',
                             f'{500+i}.png')  # Thay đổi đường dẫn theo ý bạn
    # time.sleep(5)
    # Lưu ảnh chụp
    cv2.imwrite(save_path, screenshot)
    time.sleep(2.5)


