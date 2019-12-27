#!/usr/bin/python
#coding=utf-8
from enum import Enum


class SimulationParam(Enum):
    total_step = 30
    num_row = 50
    num_col = 50
    view_width = 12
    view_height = 6
    figure_path = 'C:/Users/石海明/Desktop/Analysis20191220/abm.png'       #  保存路径,目前还没有设置
    step_interval = 0.01     #      时间间隔


class AgentStatus(Enum):
    resident = "居民"
    police = "警察"
    terrorist = "恐怖分子"
    government = "政府"


class ResidentAgent(Enum):
    density = 0.70

    violence = [0, 1, 2, 3]
    violence_init_rate = [0.1, 0.2, 0.4, 0.3]

    region = [0, 1]
    region_init_rate = [0.90, 0.10]

    extreme = [0, 1]
    extreme_init_rate = [0.8, 0.2]

    language = [0, 1, 2]
    language_bi_init = 0.2

    vision = 1
    neighbor_com_rate = 0.7               # 从可以语言共同的邻居中选出自己交流的agent的几率

    property = [0.4, 0.6]
    property_init_rate = [0.8, 0.2]

    exploited_suitable = 0.8              # 最佳相对剥夺指数
    discontent_property_threshold = 0.4
    extreme_threshold = 0.4

    extreme_org_threshold = 3             # 恐怖分子形成集体认同的阈值
    extreme_behavior_prob = 0.6

    extreme_stubborn = 0.3                # 自身教育思想的顽固程度
    extreme_education_rate = 0.4          # 教育影响占比

    property_deposit_rate = 0.8
    property_priority_distribute = 0.6    # [0.5, 1]

    joint_agent_number = 3


class PoliceAgent(Enum):
    density = 0.05
    vision = 5
    patrol_number = 3


class GovernmentAgent(Enum):
    language_edu_rate = 0.05
    # joint_resident_num = 3
    extreme_education_expect = 0.2


