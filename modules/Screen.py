import mss
import numpy as np


class Screen:
    def __init__(self, monitorId = 0):
        self.screen     = mss.mss()
        self.monitor    = self.screen.monitors[monitorId]

    def shot(self):
        return np.array(self.screen.grab(self.monitor))
