import math
import os
import time
import cv2
import screen_analysis_module as sam

import time

screenshot_original = sam.get_monitor_screen(1)
img = cv2.cvtColor(screenshot_original, cv2.COLOR_BGR2GRAY)

text = "crc32"

result = sam.find_text(img, text)
if result:
    for coord in result:
        print(coord[0], coord[1])
else:
    print(f"По запросу: {text} ничего не найдено!")

# cv2.namedWindow("result", cv2.WINDOW_NORMAL)
# cv2.setWindowProperty("result", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

t = time.process_time()
print(t)
