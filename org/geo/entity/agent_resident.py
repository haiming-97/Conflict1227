#!/usr/bin/python
#coding=utf-8
from org.geo.config.global_param import AgentStatus, ResidentAgent, SimulationParam
from org.geo.entity.agent_base import Agent, Location
from org.geo.utils import Generator
import math
import random

# init : init property / neighbor / joint_agent
# step 1 compute self state : neighbour(language/communicate) -> exploited -> discontent_property -> discontent
# step 2 transform violence and property

class Resident(Agent):

    def __init__(self, index, location, vision):
        super(Resident, self).__init__(index, location, vision, status=AgentStatus.resident.value)

        self.violence = self.init_value_by_rate(ResidentAgent.violence.value, ResidentAgent.violence_init_rate.value)
        self.region = None
        # self.region = self.init_value_by_rate(ResidentAgent.region.value, ResidentAgent.region_init_rate.value)         # [0, 1]
        self.property = self.init_value_by_rate(ResidentAgent.property.value, ResidentAgent.property_init_rate.value)

        self.extreme = self.init_value_by_rate(ResidentAgent.extreme.value, ResidentAgent.extreme_init_rate.value)        # [0,1] 极端思想情况指标
        self.language = self.extreme                        # [0,1,2]
        if Generator.rand() < ResidentAgent.language_bi_init.value:
            self.language = ResidentAgent.language.value[-1]

        self.neighbour_loc = []                            #
        self.neighbour_lan = []
        self.neighbour_com = []

        self.exploited = 0                                 # [0, 1] agent i 的相对剥夺指数

        self.discontent_property = 0
        self.discontent = 0

        self.joint_agent = []
        self.extreme_behavior_prob = ResidentAgent.extreme_behavior_prob.value
        self.terrorist = False

    def compute_neighbour(self, loc2resident,
                          communicate_rate=ResidentAgent.neighbor_com_rate.value,
                          joint_num=ResidentAgent.joint_agent_number.value):

        neighbour_loc = []
        neighbour_lan = []
        neighbour_com = []

        locations = self.location.get_location(self.vision)
        for loc in locations:
            resident = loc2resident.get(str(loc), "none")
            if resident != "none": neighbour_loc.append(resident)
        self.neighbour_loc = neighbour_loc

        for agent in self.neighbour_loc:
            if self.language == 2 or self.language == agent.language:
                neighbour_lan.append(agent)
        self.neighbour_lan = neighbour_lan

        for agent in self.neighbour_lan:
            if Generator.satisfied(communicate_rate):
                neighbour_com.append(agent)
        self.neighbour_com = neighbour_com

        joint_agent = []
        joint_indexes = Generator.unique_list(len(self.neighbour_loc), joint_num)
        for index in joint_indexes:
            joint_agent.append(self.neighbour_loc[index])
        self.joint_agent = joint_agent

    def compute_exploited(self):
        neighbour_sorted = sorted(self.neighbour_com, key=lambda agent: agent.property, reverse=False)
        # print(neighbour_sorted)
        if len(neighbour_sorted) > 0:
            denominator = 0.1
            numerator = 0.0
            for agent in neighbour_sorted:
                denominator += agent.property - neighbour_sorted[0].property
                # print(denominator)
                if agent.property > self.property:
                    numerator += agent.property - self.property
            self.exploited = numerator / denominator
        else:
            self.exploited = 0.0

    def compute_discontent(self, exploited_suitable=ResidentAgent.exploited_suitable.value):
        self.discontent_property =((self.exploited-exploited_suitable)/exploited_suitable) ** 2 #   计算生活不满意度
        self.discontent = self.discontent_property * self.extreme #   计算综合不满意指标


    def transform_violence(self):
        '''
        最终产生恐怖行为返回True
        '''
        extreme_behavior = False

        if self.region == ResidentAgent.region.value[0]:
            return extreme_behavior

        condition_property = self.discontent_property >= ResidentAgent.discontent_property_threshold.value
        condition_extreme = self.extreme >= ResidentAgent.extreme_threshold.value

        if self.violence == ResidentAgent.violence.value[0]:
            if (condition_property and not condition_extreme) or (condition_extreme and not condition_property):
                self.violence = ResidentAgent.violence.value[1]

        elif self.violence == ResidentAgent.violence.value[1]:
            if condition_property and condition_extreme:
                self.violence = ResidentAgent.violence.value[2]

        elif self.violence == ResidentAgent.violence.value[2]:
            extreme_count = 0
            for agent in self.neighbour_com:
                if agent.violence == ResidentAgent.violence.value[2]:
                    extreme_count += 1

            if extreme_count >= ResidentAgent.extreme_org_threshold.value:
                self.violence = ResidentAgent.violence.value[3]

        elif self.violence == ResidentAgent.violence.value[3]:
            if Generator.satisfied(self.extreme_behavior_prob) or self.terrorist:
                extreme_behavior = True
                self.terrorist = True
        return extreme_behavior


    def transform_property(self,
                           deposit_rate=ResidentAgent.property_deposit_rate.value,
                           priority_distribute_rate=ResidentAgent.property_priority_distribute.value):
        for agent in self.neighbour_com:
            if agent.index < self.index:
                property_delta = (1 - deposit_rate) * (self.property + agent.property)
                priority =  priority_distribute_rate * property_delta
                inferior = property_delta - priority
                prob = self.property / (self.property + agent.property)
                if Generator.satisfied(prob):
                    self.property = (self.property * deposit_rate) + priority
                    agent.property = (agent.property * deposit_rate) + inferior
                else:
                    self.property = (self.property * deposit_rate) + inferior
                    agent.property = (agent.property * deposit_rate) + priority

    def extreme_neighbor_influence(self):
        extreme_acc = 0.0
        weight_acc = 0.1
        for agent in self.neighbour_com:
            distance = 1.0
            weight = 1.0 / distance
            extreme_acc += weight * agent.extreme
            weight_acc += weight
        return extreme_acc / weight_acc


    def init_value_by_rate(self, value_list, rate_list):
        result = 0
        prob = Generator.rand()
        pre_rate = 0.0
        for index in range(len(rate_list)):
            now_rate = rate_list[index] + pre_rate
            if prob < now_rate:
                result = value_list[index]
                break
            pre_rate = now_rate
        return result


    def set_region(self):
        self.region = 1


    def set_resident(self):
        self.region = 0

