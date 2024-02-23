import os
import time
import cv2
import screen_analysis_module as sam

screenshot_original = sam.get_monitor_screen(2)

img_output_dir = 'img'

if not os.path.exists(img_output_dir):
    os.makedirs(img_output_dir)


img1 = cv2.cvtColor(screenshot_original, cv2.COLOR_BGR2GRAY)

# Список путей к изображениям
image_paths = ['icon1.png', 'icon2.png', 'icon3.png', 'icon4.png', 'icon5.png']


for image_path in image_paths:
    img2 = cv2.imread(image_path, cv2.COLOR_BGR2GRAY)
    x, y = sam.detect_img_coord(img1, img2, image_path[:-4], is_debug=False, ratio=0.3)
    if x and y:
        print(f"img name = {image_path[:-4]}, coord x={x}, coord y={y}")
    else:
        print(f"img name {image_path[:-4]} not found")

t = time.process_time()
print(t)