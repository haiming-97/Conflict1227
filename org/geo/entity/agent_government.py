#!/usr/bin/python
#coding=utf-8
from org.geo.config.global_param import AgentStatus, ResidentAgent, PoliceAgent, GovernmentAgent
from org.geo.entity.agent_base import Agent
from org.geo.utils import Generator


class Government():

    def __init__(self, loc2polices,
                 language_edu_rate=GovernmentAgent.language_edu_rate.value,
                 extreme_edu_expect=GovernmentAgent.extreme_education_expect.value):
        self.language_edu_rate = language_edu_rate
        self.extreme_edu_expect = extreme_edu_expect
        self.loc2polices = loc2polices

    def language_edu(self, agents):
        agent_list = list(agents)
        agent_number = len(agent_list) * self.language_edu_rate
        indexes = Generator.unique_list(len(agent_list), agent_number)
        for index in indexes:
            agent_list[index].language = ResidentAgent.language.value[2]
            for agent in agent_list[index].joint_agent:
                agent.language = ResidentAgent.language.value[2]

    def police_patrol(self, loc2resident):
        for police in self.loc2polices.values():
            police.compute_patrol_candidates(loc2resident)
            police.patrol_residents(self.extreme_edu_expect)



