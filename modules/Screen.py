import mss
import numpy as np

from tkinter    import Tk, Canvas
from platform   import system


class Screen:
    def __init__(   self,
                    monitorId               = 0,
                    aimSize                 = 112,
                    aimWidth                = 6,
                    aimColor                = (255, 0, 0),
                    aimDelay                = 1200,
                    aimAnimationDelay       = 20,
                    aimRootTransparentColor = '#f0f0f0',
                    aimRootAlpha            = 0.3
    ):
        self.screen                     = mss.mss()
        self.monitor                    = self.screen.monitors[monitorId]

        self.aimParams = {
            'size':                 aimSize,
            'width':                aimWidth,
            'color':                aimColor,
            'delay':                aimDelay,
            'animationDelay':       aimAnimationDelay,
        }

        if system() == 'Windows':
            self.aimParams['rootAttributes'] = ('-transparentcolor',
                                                aimRootTransparentColor)
        else:
            self.aimParams['rootAttributes'] = ('-alpha', aimRootAlpha)

        self.canvas_item_tags = []


    def shot(self):
        return np.array(self.screen.grab(self.monitor))


    def calculateNewColor(self, currentColor, direction, step=25):
        newColor = currentColor

        if direction > 0:
            if currentColor + step >= 255:
                newColor = 255
                direction = -1
            else:
                newColor += step
        else:
            if currentColor - step <= 0:
                newColor = 0
                direction = 1
            else:
                newColor -= step

        return newColor, direction
    

    def updateColor(self, canvas, item_tags, r, g, b, directionR, directionG, directionB):
        fill_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
        for tag in item_tags:
            canvas.itemconfig(tag, fill=fill_color)

        r, directionR = self.calculateNewColor(r, directionR)
        g, directionG = self.calculateNewColor(g, directionG)
        b, directionB = self.calculateNewColor(b, directionB)

        canvas.after(self.aimParams['animationDelay'], self.updateColor, canvas, item_tags, r, g, b, directionR,
                     directionG, directionB)


    def aim(self, point):
        root = Tk()
        root.geometry(f"+{self.monitor['left']}+{self.monitor['top']}")
        root.overrideredirect(True)
        root.wait_visibility(root)
        root.attributes(*self.aimParams['rootAttributes'])

        canvas = Canvas(root,
                        width   = self.monitor['width'],
                        height  = self.monitor['height'])
        canvas.pack()

        r, g, b = self.aimParams['color']
        fill_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)

        line1_tag = canvas.create_line(point[0] - self.aimParams['size'] // 2, point[1],
                                       point[0] + self.aimParams['size'] // 2, point[1],
                                       fill=fill_color, width=self.aimParams['width'])
        line2_tag = canvas.create_line(point[0], point[1] - self.aimParams['size'] // 2,
                                       point[0], point[1] + self.aimParams['size'] // 2,
                                       fill=fill_color, width=self.aimParams['width'])

        self.canvas_item_tags = [line1_tag, line2_tag]

        root.lift()
        root.update()

        directionR = 1
        directionG = 1
        directionB = 1

        canvas.after(self.aimParams['delay'], root.destroy)
        canvas.after(self.aimParams['animationDelay'], self.updateColor, canvas, self.canvas_item_tags, r, g, b,
                     directionR, directionG, directionB)

        root.mainloop()
