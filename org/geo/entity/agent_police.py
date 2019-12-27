#!/usr/bin/python
#coding=utf-8
from org.geo.config.global_param import AgentStatus, ResidentAgent, PoliceAgent
from org.geo.entity.agent_base import Agent, Location
from org.geo.config.global_param import *
from org.geo.entity.agent_resident import *
from org.geo.config.global_param import AgentStatus, ResidentAgent, SimulationParam
from org.geo.utils import Generator
import math


# patrol resident and education
class Police(Agent):

    def __init__(self, index, location, vision = PoliceAgent.vision.value):
        super(Police, self).__init__(index, location, vision, status=AgentStatus.police.value)
        self.patrol_candidates = []
        self.patrol_number = PoliceAgent.patrol_number.value
        self.patrol_targets = []

    def compute_patrol_candidates(self, loc2residents):
        candidates = []
        locations = self.location.get_location(self.vision)
        for loc in locations:
            resident = loc2residents.get(str(loc), "none")
            if resident != "none": candidates.append(resident)
        self.patrol_candidates = candidates

    def patrol_residents(self, education_expect=GovernmentAgent.extreme_education_expect.value):

        patrol_targets = []
        if len(self.patrol_candidates) <= self.patrol_number:
            patrol_targets = self.patrol_candidates
        else:
            patrol_indexes = Generator.unique_list(len(self.patrol_candidates), self.patrol_number)
            for index in patrol_indexes:
                patrol_targets.append(self.patrol_candidates[index])
        self.patrol_targets = patrol_targets

        # 联合防治
        total_targets = patrol_targets
        for agent in patrol_targets:
            total_targets = total_targets + agent.joint_agent
        for resident in total_targets:
            if resident.violence == ResidentAgent.violence.value[3]:
                resident.violence = ResidentAgent.violence.value[2]
                resident.terrorist = False
            elif resident.violence == ResidentAgent.violence.value[2]:
                self._patrol_education(resident, education_expect)# 教培
            else:
                # 1或者0不做处理
                pass

    def _patrol_education(self,
                          agent,
                          extreme_edu,
                          extreme_education_effect= ResidentAgent.extreme_education_rate.value,
                          extreme_stubborn = ResidentAgent.extreme_stubborn.value):
        # 弱化极端思想
        extreme_social = agent.extreme_neighbor_influence()
        extreme_env = extreme_education_effect * extreme_edu + (1 - extreme_education_effect) * extreme_social
        agent.extreme = extreme_stubborn * agent.extreme + (1 - extreme_stubborn) * extreme_env