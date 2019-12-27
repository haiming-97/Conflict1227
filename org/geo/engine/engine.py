#!/usr/bin/python
#coding=utf-8


from org.geo.engine.abm import Model
from org.geo.engine.time import Timer
from org.geo.utils.Log import Logger
from pynput.keyboard import Key, Listener

from org.geo.view.view import Viewer
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class Engnine:

    timer = None

    def __init__(self):

        Engnine.timer = Timer()
        self.model = Model(timer=Engnine.timer, viewer=Viewer())
        # self.listener = Listener(on_press=Engnine.press, on_release=Engnine.release)

    def run(self):

        # self.listener.start()
        # self.listener.join()
        self.model.run()

    @staticmethod
    def switch():
        Engnine.timer.switch()

    @staticmethod
    def press(key):
        if key == Key.space:
            Engnine.switch()

    @staticmethod
    def release(key):
        if key == Key.esc:
            return False


if __name__ == "__main__":
    # logger = Logger().getLogger()
    engine = Engnine()
    engine.run()





