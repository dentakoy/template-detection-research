import time
from tkinter import Tk, Canvas
from window_module import get_monitor_info


def draw_cross(cross_x: int, cross_y: int, cross_size: int = 15, cross_width: int = 3, R: int = 255, G: int = 0,
               B: int = 0, delay: int = 1200, anim_delay: int = 20):
    direction_R = 1
    direction_G = 1
    direction_B = 1
    root = Tk()
    root.geometry("+0+0")
    root.overrideredirect(True)
    root.wait_visibility(root)
    root.attributes('-transparentcolor', '#f0f0f0')

    monitor = get_monitor_info()
    print(monitor)
    monitor_width = monitor['width']
    monitor_height = monitor['height']

    canvas = Canvas(root, width=monitor_width, height=monitor_height)
    canvas.pack()

    fill_color = '#{:02x}{:02x}{:02x}'.format(R, G, B)

    canvas.create_line(cross_x - cross_size // 2, cross_y, cross_x + cross_size // 2, cross_y, fill=fill_color,
                       width=cross_width)
    canvas.create_line(cross_x, cross_y - cross_size // 2, cross_x, cross_y + cross_size // 2, fill=fill_color,
                       width=cross_width)
    root.lift()
    root.update()

    def update_color():
        nonlocal R, G, B, direction_R, direction_G, direction_B, fill_color
        R, direction_R = calculate_new_color(R, direction_R)
        G, direction_G = calculate_new_color(G, direction_G)
        B, direction_B = calculate_new_color(R, direction_B)
        fill_color = '#{:02x}{:02x}{:02x}'.format(R, G, B)
        canvas.itemconfig(1, fill=fill_color)
        canvas.itemconfig(2, fill=fill_color)
        root.after(anim_delay, update_color)

    def close_window():
        root.destroy()

    t = time.process_time()
    print(t)
    root.after(delay, close_window)
    root.after(anim_delay, update_color)

    root.mainloop()


def calculate_new_color(current_color, direction, step=25):
    new_color = current_color

    if direction > 0:
        if current_color + step >= 255:
            new_color = 255
            direction = -1
        else:
            new_color += step
    else:
        if current_color - step <= 0:
            new_color = 0
            direction = 1
        else:
            new_color -= step

    return new_color, direction
