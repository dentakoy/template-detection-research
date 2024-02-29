from typing import Tuple
import win32gui
import math
import cv2
import numpy as np
from mss import mss
import os
import easyocr


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
    img_original = None
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
        box = []
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
            point = [point_x, point_y]
            box.append(point)

            if is_debug:
                draw_cross(img_cross, point_x, point_y, G=155, size=20)

        # Рассчет средних координат x и y
        average_x = int(sum_x / num_points)
        average_y = int(sum_y / num_points)
        box = list(map(list, set(map(tuple, box))))
        if len(box) > 2:
            average_x, average_y = centroid(box)

        if is_debug:
            print(f"Average Coordinates: (x={average_x}, y={average_y})")
            draw_cross(img_cross, average_x, average_y, G=255, R=0, B=122, size=20)
            cv2.imwrite(f'{img_output_dir}{os.path.sep}{img2_name}.png', img_cross)
        return average_x, average_y
    else:
        if is_debug:
            print(f"{img2_name}, не найдено совпадений")
        return None, None


def centroid(vertices) -> tuple[int, int]:
    x, y = 0, 0
    n = len(vertices)
    print(n, vertices)
    signed_area = 0
    for i in range(n):
        x0, y0 = vertices[i]
        x1, y1 = vertices[(i + 1) % n]
        # shoelace formula
        area = (x0 * y1) - (x1 * y0)
        signed_area += area
        x += (x0 + x1) * area
        y += (y0 + y1) * area
    signed_area *= 0.5
    x /= 6 * signed_area
    y /= 6 * signed_area
    return int(x), int(y)


def find_text(img, string: str):
    text_coord_array = []
    reader = easyocr.Reader(['ru', 'en'])
    result = reader.readtext(img)
    string = string.casefold()
    for detection in result:
        box = detection[0]
        text = detection[1].casefold()
        if string not in text.casefold():
            continue
        centr_x, centr_y = centroid(box)
        text_coord_array.append([centr_x, centr_y])

    return text_coord_array


def get_window_title_coord(window_name: str, scale_factor: float = 1.0):
    def callback(handle, data):
        nonlocal visible_rect
        if window_name.casefold() in win32gui.GetWindowText(handle).casefold():
            client_rect = win32gui.GetClientRect(handle)
            client_top_left = client_rect[:2]
            client_bottom_right = client_rect[2:]
            visible_top_left = win32gui.ClientToScreen(handle, client_top_left)
            visible_bottom_right = win32gui.ClientToScreen(handle, client_bottom_right)
            visible_rect = (*visible_top_left, *visible_bottom_right)  # Convert to a single rect tuple

    visible_rect = None
    win32gui.EnumWindows(callback, None)

    if visible_rect is not None:
        visible_rect = tuple(math.ceil(coord * scale_factor) for coord in visible_rect)

    return visible_rect
