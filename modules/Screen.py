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

        r, g, b     = self.aimParams['color']
        fill_color  = '#{:02x}{:02x}{:02x}'.format(r, g, b)

        canvas.create_line( point[0] - self.aimParams['size'] // 2, point[1],
                            point[0] + self.aimParams['size'] // 2, point[1],
                            fill=fill_color, width=self.aimParams['width'])
        
        canvas.create_line( point[0], point[1] - self.aimParams['size'] // 2,
                            point[0], point[1] + self.aimParams['size'] // 2,
                            fill=fill_color, width=self.aimParams['width'])
        root.lift()
        root.update()

        directionR = 1
        directionG = 1
        directionB = 1

        def updateСolor():
            nonlocal r, g, b, directionR, directionG, directionB, fill_color
            r, directionR = self.calculateNewColor(r, directionR)
            g, directionG = self.calculateNewColor(g, directionG)
            b, directionB = self.calculateNewColor(b, directionB)
            fill_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
            canvas.itemconfig(1, fill=fill_color)
            canvas.itemconfig(2, fill=fill_color)
            root.after(self.aimParams['animationDelay'], updateСolor)

        root.after(self.aimParams['delay'],             root.destroy)
        root.after(self.aimParams['animationDelay'],    updateСolor)
        root.mainloop()
