from typing import Tuple

import cv2
import numpy as np
from mss import mss
import os


def get_monitor_screen(monitor_number: int = 1) -> object:
    # Инициализация объекта mss для захвата экрана
    sct = mss()

    # Получение размеров экрана
    monitor = sct.monitors[monitor_number]

    # Захват скриншота
    sct_img = sct.grab(monitor)
    screenshot = np.array(sct_img)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
    return screenshot


def draw_cross(img, point_x: int, point_y: int, R: int = 255, G: int = 0, B: int = 0, size: int = 10):
    cross_color = (B, G, R)
    cross_size = size  # Размер креста
    # Отображение креста на изображении
    cv2.line(img, (int(point_x - cross_size), int(point_y)),
             (int(point_x + cross_size), int(point_y)), cross_color, 2)
    cv2.line(img, (int(point_x), int(point_y - cross_size)),
             (int(point_x), int(point_y + cross_size)), cross_color, 2)


def detect_img_coord(img1, img2, img2_name: str, is_gray: bool = True, ratio: float = 0.4, img_output_dir: str = 'img',
                     is_debug: bool = True) -> tuple[int, int]:
    if not is_gray:
        img_original = img1
        img1 = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)

    # -- Step 1: Detect the keypoints using SURF Detector, compute the descriptors
    detector = cv2.SIFT_create()

    kp1, des1 = detector.detectAndCompute(img1, None)
    kp2, des2 = detector.detectAndCompute(img2, None)

    matcher = cv2.BFMatcher()
    matches = matcher.knnMatch(des1, des2, 2)

    threshold_ratio = ratio
    filtered_matches = []

    for match in matches:
        if match[0].distance < threshold_ratio * match[1].distance:
            filtered_matches.append(match[0])

    good_matches = sorted(filtered_matches, key=lambda x: x.distance)[:4]

    if len(good_matches) > 0:

        if is_debug:
            print(f"len matches {len(good_matches)}")
        # Инициализация сумм координат и подсчет количества точек
        sum_x = 0
        sum_y = 0
        num_points = len(good_matches)
        if is_gray:
            img_cross = np.copy(img1)
        else:
            img_cross = np.copy(img_original)
        # Проход по всем точкам и накопление сумм координат

        for match in good_matches:
            # координата x точки из первого изображения
            sum_x += kp1[match.queryIdx].pt[0]
            # координата y точки из первого изображения
            sum_y += kp1[match.queryIdx].pt[1]
            point_x = kp1[match.queryIdx].pt[0]
            point_y = kp1[match.queryIdx].pt[1]

            if is_debug:
                draw_cross(img_cross, point_x, point_y, G=155, size=20)

        # Рассчет средних координат x и y
        average_x = int(sum_x / num_points)
        average_y = int(sum_y / num_points)

        if is_debug:
            print(f"Average Coordinates: (x={average_x}, y={average_y})")
            cv2.imwrite(f'{img_output_dir}{os.path.sep}{img2_name}.png', img_cross)
        return average_x, average_y
    else:
        if is_debug:
            print(f"{img2_name}, не найдено совпадений")
        return None, None
