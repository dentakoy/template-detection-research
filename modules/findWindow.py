from platform import system
import re


class FindWindow:
    def __init__(self, titleTemplate={}):
        self.titleTemplate = {}
        for key in titleTemplate:
            keyResult = self.find(key)
            if keyResult:
                # print(keyResult)
                for k in keyResult:
                    self.titleTemplate.setdefault(key.pattern, []).append({
                        'title': k[0],
                        'coords': k[1]
                    })

    def getResult(self):
        return self.titleTemplate

    def getLinuxTitleCoords(self, title_pattern: re.Pattern):
        from collections import namedtuple
        import Xlib.display
        MyGeom = namedtuple('MyGeom', 'x y height width')

        disp = Xlib.display.Display()
        root = disp.screen().root

        NET_CLIENT_LIST = disp.intern_atom('_NET_CLIENT_LIST')
        UTF8_STRING = disp.intern_atom('UTF8_STRING')

        def get_absolute_geometry(win):
            """
            Returns the (x, y, height, width) of a window relative to the top-left
            of the screen.
            """
            geom = win.get_geometry()
            (x, y) = (geom.x, geom.y)
            while True:
                parent = win.query_tree().parent
                pgeom = parent.get_geometry()
                x += pgeom.x
                y += pgeom.y
                if parent.id == root.id:
                    break
                win = parent
            return MyGeom(x, y, geom.height, geom.width)

        def get_window_bbox(win):
            """
            Returns (x1, y1, x2, y2) relative to the top-left of the screen.
            """
            geom = get_absolute_geometry(win)
            x1 = geom.x
            y1 = geom.y
            x2 = x1 + geom.width
            y2 = y1 + geom.height
            return ((x1, y1), (x2, y2))

        def get_window_title_coord(window_name_pattern: re.Pattern):
            window_title_and_coords = []

            window_list = root.get_full_property(NET_CLIENT_LIST, 0).value

            for window in window_list:
                window_obj = disp.create_resource_object('window', window)

                window_title = window_obj.get_full_property(disp.intern_atom('_NET_WM_NAME'), UTF8_STRING).value.decode(
                    'utf-8')
                # print(window_title)
                if window_title and window_name_pattern.search(window_title):
                    # print(window_title, get_window_bbox(window_obj))
                    window_title_and_coords.append([window_title, get_window_bbox(window_obj)])

            return window_title_and_coords

        return get_window_title_coord(title_pattern)

    def getWindowsTitleCoords(self, title_pattern: re.Pattern):
        from tkinter import Tk
        from screeninfo import get_monitors
        import win32gui

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

        get_scale_factor()

        def get_window_title_coord(window_name_pattern: re.Pattern, scale_factor: float = 1.0, isVisibleRect: bool = True):

            window_title_and_coords = []

            def callback(handle, data):
                if window_name_pattern.search(win32gui.GetWindowText(handle)):
                    window_title = win32gui.GetWindowText(handle)
                    # print(win32gui.GetWindowText(handle))
                    client_rect = win32gui.GetClientRect(handle)
                    client_top_left = client_rect[:2]
                    # print(f"client top left = {client_top_left}")
                    client_bottom_right = client_rect[2:]
                    # print(f"client bottom right = {client_bottom_right}")

                    if isVisibleRect:
                        visible_top_left = win32gui.ClientToScreen(handle, client_top_left)
                        # print(f"visible top right = {visible_top_left}")
                        visible_bottom_right = win32gui.ClientToScreen(handle, client_bottom_right)
                        # print(f"visible top right = {visible_bottom_right}")
                        # print(visible_top_left, visible_bottom_right)
                        rect = (visible_top_left, visible_bottom_right)
                    else:
                        rect = (client_top_left, client_bottom_right)
                    window_title_and_coords.append([window_title, rect])

            win32gui.EnumWindows(callback, None)

            return window_title_and_coords

        return get_window_title_coord(title_pattern)

    def find(self, title_pattern: re.Pattern):
        if system() == 'Windows':
            return self.getWindowsTitleCoords(title_pattern)
        elif system() == 'Linux':
            return self.getLinuxTitleCoords(title_pattern)
