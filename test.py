import cv2

import numpy as np
from mss import mss
import time

# time.sleep(2)
# Инициализация объекта mss для захвата экрана
sct = mss()

# Получение размеров экрана
monitor = sct.monitors[2]

# Захват скриншота
sct_img = sct.grab(monitor)
screenshot = np.array(sct_img)
screenshot_original = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)


img1 = cv2.cvtColor(screenshot_original, cv2.COLOR_BGR2GRAY)

# Список путей к изображениям
image_paths = ['icon1.png', 'icon2.png', 'icon3.png', 'icon4.png', 'icon5.png']


matching_type = 'flann'
for image_path in image_paths:
    img2 = cv2.imread(image_path)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img2 = gray2

    # -- Step 1: Detect the keypoints using SURF Detector, compute the descriptors
    SIFT = cv2.SIFT_create()
    detector = SIFT

    kp1, des1 = detector.detectAndCompute(img1, None)
    kp2, des2 = detector.detectAndCompute(img2, None)
    # -- Step 2: Matching descriptor vectors with a FLANN based matcher
    # Since SURF is a floating-point descriptor NORM_L2 is used
    index_params = dict(algorithm=1, trees=5)
    search_params = dict(checks=50)
    matcher = cv2.FlannBasedMatcher(index_params, search_params)
    matches = matcher.knnMatch(des1, des2, 2)
    
    # -- Filter matches using the Lowe's ratio test
    # ratio_thresh = 0.5
    # good_matches = []
    # for m in matches:
    #     query_idx = m.queryIdx
    #     train_idx = m.trainIdx
    #     distance = m.distance
        
    #     # Do your ratio test here
    #     if matches[query_idx].distance < ratio_thresh * matches[train_idx].distance:
    #         good_matches.append(m)

    threshold_ratio     = 0.8
    filtered_matches    = []

    for match in matches:
        if match[0].distance < threshold_ratio * match[1].distance:
            filtered_matches.append(match[0])

    good_matches = sorted(filtered_matches, key=lambda x: x.distance)[:4]

    if len(good_matches) > 0:
        print(f"len matches {len(good_matches)}")
        # Инициализация сумм координат и подсчет количества точек
        sum_x = 0
        sum_y = 0
        num_points = len(good_matches)

        # Проход по всем точкам и накопление сумм координат
        img_cross = np.copy(screenshot_original)
        for match in good_matches:
            # координата x точки из первого изображения
            sum_x += kp1[match.queryIdx].pt[0]
            # координата y точки из первого изображения
            sum_y += kp1[match.queryIdx].pt[1]
            point_x = kp1[match.queryIdx].pt[0]
            point_y = kp1[match.queryIdx].pt[1]
            height, width = screenshot_original.shape[:2]
            
            cross_color = (0, 0, 255)  # Зеленый цвет
            cross_size = 10  # Размер креста
                    # # Отображение креста на изображении
            cv2.line(img_cross, (int(point_x - cross_size), int(point_y)),
                 (int(point_x + cross_size), int(point_y)), cross_color, 2)
            cv2.line(img_cross, (int(point_x), int(point_y - cross_size)),
                 (int(point_x), int(point_y + cross_size)), cross_color, 2)

        # Рассчет средних координат x и y
        average_x = int(sum_x / num_points)
        average_y = int(sum_y / num_points)

        print(f"Average Coordinates: (x={average_x}, y={average_y})")


        cv2.imwrite(
            f'img/{image_path[:-4]}.png', img_cross)
    else:
        print(
            f"{image_path[:-4]}, не найдено совпадений")

t = time.process_time()
print(t)