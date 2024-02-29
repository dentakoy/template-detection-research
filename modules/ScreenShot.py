import mss
import numpy as np


class ScreenShot:
    def __init__(self, monitorId):
        self.screen     = mss.mss()
        self.monitor    = self.screen.monitors[monitorId]

    def take(self):
        return np.array(self.screen.grab(self.monitor))
