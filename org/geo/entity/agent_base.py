#!/usr/bin/python
#coding=utf-8
import math
from org.geo.config.global_param import *


class Agent:
    def __init__(self, index, location, vision, status):
        self.index = index
        self.location = location
        self.vision = vision
        self.status = status

    def __str__(self):
        return '[index:%s   loc:%s   status:%s]' % (self.index, self.location, self.status)


class Location:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def get_location(self, vision, max_row=SimulationParam.num_row.value - 1, max_col=SimulationParam.num_col.value - 1):
        locations = []
        row = self.row
        col = self.col
        row_min = max(row - vision, 0)
        row_max = min(row + vision, max_row)
        col_min = max(col - vision, 0)
        col_max = min(col + vision, max_col)
        for neighbour_row in range(row_min, row_max + 1):
            for neighbour_col in range(col_min, col_max + 1):
                if 0 < abs(neighbour_row - row) + abs(neighbour_col - col) <= vision:  # calculate distance
                    locations.append(Location(neighbour_row, neighbour_col))
        return locations

    def __str__(self):
        return '(%s, %s)' % (self.row, self.col)