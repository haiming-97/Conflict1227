#!/usr/bin/python
#coding=utf-8
import os

import matplotlib.pyplot as plt
from org.geo.config.global_param import SimulationParam, ResidentAgent
from org.geo.utils import Generator



class Viewer:

    def __init__(self, width=SimulationParam.view_width.value, height=SimulationParam.view_height.value):
        grid = plt.GridSpec(4, 4, wspace=0.5, hspace=0.8)

        self.fig = plt.figure(num='ABM', figsize=(12, 6))
        plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)
        plt.ion()


        self.agent_ax = plt.subplot(grid[0:4, 0:2])
        # self.color = {'0':'#acc2d9', '1':'#a2cffe', '2':'#3778bf', '3':'#042e60',
        #                    '9':'red', 'police':'green'}
        self.color = {'0': '#3778bf', '1': '#3778bf', '2': '#3778bf', '3': '#3778bf',
                      'region': '#38044B', '9': '#FF0000', 'police': '#048243'}
        self.marker = {'0': 's', '1': 's', '2': 's', '3': 's', 'region': 'o', '9': 's', 'police': 'p'}
        self.label = {'0': 'level 1', '1': 'level 2', '2': 'level 3', '3': 'level 4',
                      'region': 'region', '9': 'terrorist',  'police': 'police'}

        self.resident_size = 24
        self.police_size = 14
        self.region_size = 4

        self.terrorist_ax = plt.subplot(grid[0:2, 2:4])
        self.terrorist_ax.set_title("cumulative number of terrorists", fontsize=10)
        self.terrorist_ax.set_xticks([])
        self.terrorist_ax.set_yticks([])

        self.property_ax = plt.subplot(grid[2:4, 2:4])
        self.property_ax.set_title("distribution of property", fontsize=10)
        self.property_ax.set_xticks([])
        self.property_ax.set_yticks([])


    def render(self, data=None):
        self.agent_ax.cla()
        # self.agent_ax.scatter(data['resident_x'], data['resident_y'],
        #                       c=self.color.get('0'),
        #                       marker=self.marker.get('0'),
        #                       label=self.label.get('0'),
        #                       s=self.resident_size)
        for (x, y, s) in zip(data['resident_x'], data['resident_y'], data['resident_violence']):
            self.agent_ax.scatter(x, y,
                                   c=self.color.get(s),
                                   marker=self.marker.get(s),
                                   label=self.label.get(s),
                                   alpha=1,
                                   s=self.resident_size)
        self.agent_ax.scatter(data['region_x'], data['region_y'],
                              c=self.color.get('region'),
                              marker=self.marker.get('region'),
                              label=self.label.get('region'),
                              alpha=1,
                              s=self.region_size)
        self.agent_ax.scatter(data['police_x'], data['police_y'],
                              c=self.color.get('police'),
                              marker=self.marker.get('police'),
                              label=self.label.get('police'),
                              s=self.police_size)
        self.agent_ax.set_title("step : %d "%(data['current_step']), fontsize=10, fontweight='bold')
        self.no_spines(self.agent_ax)
        # self.agent_ax.legend()

        self.terrorist_ax.cla()
        x = [x+1 for x in range(len(data['extreme_event_count']))]
        self.terrorist_ax.plot(x, data['extreme_event_count'], 'ro-', linewidth=1.6, markersize=3, c='#9e3623')
        self.terrorist_ax.set_xlim(1, data['total_step'])
        self.terrorist_ax.set_ylim(0, 2500)
        self.terrorist_ax.set_title("cumulative number of terrorists", fontsize=10)
        self.terrorist_ax.tick_params(labelsize=8)

        self.property_ax.cla()
        self.property_ax.hist(data['resident_property'], bins=20, histtype="stepfilled")
        self.property_ax.set_title("distribution of property", fontsize=10)
        self.property_ax.tick_params(labelsize=8)

        plt.pause(SimulationParam.step_interval.value)

        if data['current_step'] == data['total_step']:
            path = SimulationParam.figure_path.value
            return_path = Generator.check_filename_available(path)
            plt.savefig(fname=return_path, format='png', transparent=True, dpi=1000, pad_inches=0)

    def no_spines(self, ax):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])







