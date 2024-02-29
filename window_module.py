from tkinter import Tk
from screeninfo import get_monitors


def get_monitor_info():
    monitors_info = []

    for m in get_monitors():
        # print(m)

        monitors_info.append({
            'x': m.x,
            'y': m.y,
            'width': m.width,
            'height': m.height,
            'name': m.name,
        })

    # print(len(monitors_info))
    return monitors_info[0]


def get_scale_factor(is_debug: bool = False) -> float:
    root = Tk()
    root.overrideredirect(True)
    root.wait_visibility(root)
    root.attributes('-transparentcolor', '#f0f0f0')

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    monitor = get_monitor_info()
    monitor_width = monitor['width']
    monitor_height = monitor['height']
    scale_factor_width = monitor_width / screen_width
    scale_factor_height = monitor_height / screen_height
    if is_debug:
        print(monitor_width, monitor_height, scale_factor_width, scale_factor_height)

    scale_factor = 1.0

    if scale_factor_height == scale_factor_width:
        scale_factor = scale_factor_width

    root.destroy()

    return scale_factor
