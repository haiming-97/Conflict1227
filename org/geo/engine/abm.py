#!/usr/bin/python
#coding=utf-8

from org.geo.entity.agent_base import *
from org.geo.entity.agent_government import Government
from org.geo.entity.agent_police import Police
from org.geo.entity.agent_resident import *
from org.geo.utils import Generator
from org.geo.utils.Log import Logger
import copy
from org.geo.utils import pick_index

logger = Logger().getLogger()

class Model:

    # initialize model parameter
    def __init__(self, total_step=SimulationParam.total_step.value, timer=None, viewer=None):
        self.total_step = total_step
        self.extreme_event_count = 0
        # self.timer = timers
        self.viewer = viewer
        self.row_num = SimulationParam.num_row.value
        self.col_num = SimulationParam.num_col.value
        self.index2loc = self.init_location(self.row_num, self.col_num)

        self.loc2residents, self.loc2region_residents,self.government = \
            self.init_agent(self.index2loc, PoliceAgent.density.value, ResidentAgent.density.value)


    def init_location(self, row_num, col_num):
        index2loc = {}
        index_count = 0
        for row in range(row_num):
            for col in range(col_num):
                loc = Location(row, col)
                index2loc[index_count] = loc
                index_count += 1
        return index2loc


    def init_agent(self, index2loc, police_density, resident_density):
        loc2polices = {}
        loc2residents = {}
        loc2region_residents = {}

        max_index = self.row_num * self.col_num
        police_num = max_index * police_density
        police_loc_indexes = Generator.unique_list(max_index, police_num)
        Generator.write_list(list1=police_loc_indexes, filename='police')
        # police_loc_indexes = Generator.read_excel('C:/Users/石海明/Desktop/testlist/police_0.xls')
        for index in range(len(police_loc_indexes)):
            loc = index2loc[police_loc_indexes[index]]
            police = Police(index, loc)
            loc2polices[str(loc)] = police

        resident_num = max_index * resident_density
        resident_loc_indexes = Generator.unique_list(max_index, resident_num)
        Generator.write_list(list1=resident_loc_indexes, filename='resident')
        # resident_loc_indexes = Generator.read_excel('C:/Users/石海明/Desktop/testlist/resident_0.xls')
        pick_list = pick_index.pick_zone(row_max=SimulationParam.num_row.value, col_max=SimulationParam.num_col.value,
                                         zone=[3, 3, 5])
        all_list = pick_index.all_zone(row_max=SimulationParam.num_row.value, col_max=SimulationParam.num_col.value)
        # print(all_list)
        region_list = Generator.unique_pick_list(pick_list, resident_num * ResidentAgent.region_init_rate.value[1])
        extral_list = list(set(all_list).difference(set(region_list)))
        resident_list = Generator.unique_pick_list(extral_list, resident_num * ResidentAgent.region_init_rate.value[0])
        # print(resident_list)
        # print(region_list)
        # for index in range(len(resident_loc_indexes)):
        #     loc = index2loc[resident_loc_indexes[index]]
        #     resident = Resident(index, loc, vision=1)
        #     loc2residents[str(loc)] = resident
        for index in range(len(resident_list)):
            loc = index2loc[resident_list[index]]
            resident = Resident(index, loc, vision=1)
            loc2residents[str(loc)] = resident
        for index in range(len(region_list)):
            region_loc = index2loc[region_list[index]]
            resident = Resident(index, region_loc, vision=1)
            loc2region_residents[str(region_loc)] = resident
        return loc2residents, loc2region_residents, Government(loc2polices)

    def run(self):
        # render data
        step_list = []
        event_list = []
        view_data = {}
        view_data['total_step'] = self.total_step
        police_x = []
        police_y = []
        for police in self.government.loc2polices.values():
            police_x.append(police.location.col)
            police_y.append(police.location.row)
        view_data['police_x'] = police_x
        view_data['police_y'] = police_y
        view_data['extreme_event_count'] = [self.extreme_event_count]

        for step in range(self.total_step):
            step += 1
            step_list.append(step)
            event_list.append(self.extreme_event_count)
            loc2residents = copy.copy(self.loc2residents)
            loc2region_residents = copy.copy(self.loc2region_residents)

            # render data
            resident_x = []
            resident_y = []
            resident_property = []
            resident_violence = []
            resident_terrorist = []
            resident_region = []
            region_x = []
            region_y = []
            self.government.language_edu(loc2residents.values())
            for location, resident in loc2region_residents.items():
                resident.set_region()
                resident.compute_neighbour(loc2residents)
                resident.transform_property()
                resident.compute_exploited()
                resident.compute_discontent()
                is_terrorist = resident.transform_violence()
                if is_terrorist:
                    self.extreme_event_count += 1
                # render data
                resident_x.append(resident.location.col)
                resident_y.append(resident.location.row)
                resident_property.append(resident.property)
                if resident.region == 1:
                    region_x.append(resident.location.row)
                    region_y.append(resident.location.col)
                if is_terrorist:
                    resident_violence.append('9')
                else:
                    resident_violence.append(str(resident.violence))
            for location, resident in loc2residents.items():
                resident.set_resident()
                resident.compute_neighbour(loc2residents)
                resident.transform_property()
                resident.compute_exploited()
                resident.compute_discontent()
                is_terrorist = resident.transform_violence()
                if is_terrorist:
                    self.extreme_event_count += 1
                # render data
                resident_x.append(resident.location.col)
                resident_y.append(resident.location.row)
                resident_property.append(resident.property)
                if resident.region == 1:
                    region_x.append(resident.location.row)
                    region_y.append(resident.location.col)
                if is_terrorist:
                    resident_violence.append('9')
                else:
                    resident_violence.append(str(resident.violence))

            # for location, resident in loc2region_residents.items():
            #     resident.set_region()
            #     resident.compute_neighbour(loc2residents)
            #     resident.transform_property()
            #     resident.compute_exploited()
            #     resident.compute_discontent()
            #     is_terrorist = resident.transform_violence()
            #     if is_terrorist:
            #         self.extreme_event_count += 1
            #     # render data
            #         resident_x.append(resident.location.col)
            #         resident_y.append(resident.location.row)
            #         resident_property.append(resident.property)
            #     if is_terrorist:
            #         resident_violence.append('9')
            #     else:
            #         resident_violence.append(str(resident.violence))
                    # resident_x.remove(resident.location.row)
                    # resident_y.remove(resident.location.col)

            view_data['resident_x'] = resident_x
            view_data['resident_y'] = resident_y
            view_data['resident_property'] = resident_property
            view_data['resident_violence'] = resident_violence
            view_data['resident_terrorist'] = resident_terrorist
            view_data['extreme_event_count'].append(self.extreme_event_count)
            view_data['current_step'] = step
            view_data['resident_region'] = resident_region
            view_data['region_x'] = region_x
            view_data['region_y'] = region_y
            self.viewer.render(view_data)

            self.government.police_patrol(loc2residents)
            self.loc2residents = loc2residents
            print("step : %d %d"%(step, self.extreme_event_count))
        Generator.write_excel(name1='step', name2='extreme_event_count', list1=step_list,
                              list2=event_list, filename='ABM')
        # Generator.write_excel(name1='step', name2='resident_property', name3='resident_violence', name4='resident_terrorist', name5='extreme_event_count', list1=step_list_new, list2=resident_property_new, list3=resident_violence_new, list4=resident_terrorist_new, list5=event_count_new, filename='ABM')



