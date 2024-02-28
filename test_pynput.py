import math
from pynput.mouse import Controller, Button
from pynput.keyboard import Controller as KeyboardController, Key
import cv2
import screen_analysis_module as sam
import random
import time
from draw_cross_module import draw_cross

# Создаем объект контроллера мыши и клавиатуры
mouse = Controller()
keyboard = KeyboardController()
random.seed()
draw_cross(200, 200, cross_size=200, anim_delay=20)
mouse.position = (200, 200)
mouse.click(Button.left, 1)
time.sleep(0.1)
# draw_cross(200, 200, cross_size=200, anim_delay=20)

# exit(0)
text_to_type = "Hello, World! Привет Мир"
for char in text_to_type:
    keyboard.press(char)
    delay = random.uniform(0.1, 0.5)  # Генерировать случайную задержку между вводом символов
    time.sleep(delay)
    keyboard.release(char)
    delay = random.uniform(0.1, 0.5)  # Генерировать случайную задержку между вводом символов
    time.sleep(delay)
