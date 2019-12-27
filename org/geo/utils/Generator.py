#!/usr/bin/python
# coding=utf-8
import os
import xlwt
import numpy as np

import random
import xlrd

def satisfied(prob):
    return random.random() < prob

def rand():
    return random.random()

def select(a, b):
    return random.randint(a, b)


def normal(mu, sigma):
    return random.normalvariate(mu=mu, sigma=sigma)


def unique_list(max_num, size):
    origin_list = [i for i in range(max_num)]
    if max_num <= size: return origin_list
    indexes = []
    new_list = origin_list
    count = 0
    while count < size:
        value = np.random.choice(new_list)
        indexes.append(value)
        new_list.remove(value)
        count += 1
    return indexes


def unique_pick_list(origin_list, size):
    if len(origin_list) <= size: return origin_list
    indexes = []
    new_list = origin_list
    count = 0
    while count < size:
        value = np.random.choice(new_list)
        indexes.append(value)
        new_list.remove(value)
        count += 1
    return indexes


def check_filename_available(filename):
    n = [0]

    def check_meta(file_name):
        file_name_new = file_name
        if os.path.isfile(file_name):
            file_name_new = file_name[:file_name.rfind('.')] + '_' + str(n[0]) + file_name[file_name.rfind('.'):]
            n[0] += 1
        if os.path.isfile(file_name_new):
            file_name_new = check_meta(file_name)
        return file_name_new

    return_name = check_meta(filename)
    return return_name


def write_excel(name1, name2, list1, list2, filename):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'conflict', cell_overwrite_ok=True)
    name = [str(name1), str(name2)]
    path = 'C:/Users/石海明/Desktop/testexcel20191220/'+str(filename)+'.xls'
    for i in range(0, len(name)):
        sheet1.write(0, i, name[i])
    for i in range(0, len(list1)):
        sheet1.write(i+1, 0, list1[i])
    for i in range(0, len(list2)):
        sheet1.write(i+1, 1, list2[i])
    return_path = check_filename_available(path)
    f.save(return_path)


def write_list(list1, filename):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'conflict', cell_overwrite_ok=True)
    path = 'C:/Users/石海明/Desktop/testlist/'+str(filename)+'.xls'
    for i in range(0, len(list1)):
        sheet1.write(i, 0, str(list1[i]))
    return_path = check_filename_available(path)
    f.save(return_path)


def read_excel(excel_path):
    data = xlrd.open_workbook(excel_path)
    list = []
    table = data.sheets()[0]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    for i in range(0,nrows):
        rowValues = table.row_values(i) #某一行数据
        for item in rowValues:
            list.append(int(item))
    return list




