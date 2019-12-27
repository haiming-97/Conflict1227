#!/usr/bin/python
#coding=utf-8

class Timer:

    def __init__(self):
        self.is_run = False

    def switch(self):
        self.is_run = bool(1 - self.is_run)