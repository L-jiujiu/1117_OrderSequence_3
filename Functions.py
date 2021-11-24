# -*- coding:utf-8 -*-
"""
作者：l_jiujiu
日期：2021.11.17
"""
import random
import operator
import numpy as np
import pandas as pd


from prettytable import PrettyTable
from prettytable import from_csv
from Class import Sku, Section, Order, Time,CostList



# 读表格数据
def Func_ReadCsv_SkuTime(path_sku_time_map, num_sku):
    sku_time_list=[]
    data = np.genfromtxt(path_sku_time_map,
                         delimiter=",")  # 打开Excel文件
    for i in range(0, num_sku):
        sku_time_list.append(data[1, i + 1])
    return sku_time_list

def Func_ReadCsv_SkuSection(i, num_section, data, section_list):
    sku_location_num_list = []  # sku的全部所在分区（数字）
    sku_location_list = []  # sku的全部所在分区（实例）
    temp = []

    # 读取所有数据，统计为1的列目标是在该分区
    for z in range(0, num_section):
        temp.append(data[z + 1, i + 1])
        if (((temp[z]) != 0)):
            sku_location_num_list.append(z)
    # 将分区信息记录在sku对应分区的列表中

    for f in range(len(sku_location_num_list)):
        sku_location_list.append(section_list[sku_location_num_list[f]])
        # print("sku_%d" % i, "所在的分区为：%s" % sku_location_list[f].name)
    return sku_location_list

def Func_ReadCsv_SkuOrder(i,num_sku,data,section_list,sku_list):
    order_sku_num_list = []  # order中含有的sku的序号
    order_sku_number_list = []  # order中各sku序号对应的数量
    temp = []  # 用于临时存放第i行ordersku列表中不为0的列，即对应的sku信息

    # 读取所有数据，统计为1的列目标是在该分区
    for z in range(0, num_sku):
        temp.append(data[i + 1, z + 1])
        if (temp[z] != 0):
            order_sku_num_list.append(z)
            order_sku_number_list.append(temp[z])

    work_schedule = {'0':0,'1':0,'-1':0,'2':0,'3':0,'-2':0,'4':0,'5':0}
    # 将分区信息记录在sku对应分区的列表中
    for section in section_list:
        order_section_time = 0
        for num in range(len(order_sku_num_list)):
            if (sku_list[order_sku_num_list[num]].sku_location_list[0].name == section.name):
                order_section_time = order_section_time + sku_list[order_sku_num_list[num]].sku_time * \
                                     order_sku_number_list[num]

        work_schedule[str(section.num)]=order_section_time

    for i in range(6):
        if (work_schedule[str(i)]==0):
            work_schedule.pop(str(i))

    return work_schedule


def Func_Cost_sequence(order_can,section_list,order_list):
    cost = []
    for i in range(len(order_can)):
        order_can[i].Cost_cal(section_list=section_list)
        cost_input = {
            'name': order_can[i].name,  # order名
            'order': 0,  # 即将进行的订单序号
            'cost': order_can[i].weighted_cost,  # cost
            'orderfororder': i,  # 原本的序号
        }
        cost.append(CostList(cost_input))
    # 对成本以cost为键排序
    sortkey = operator.attrgetter('cost')
    cost.sort(key=sortkey)

    for i in range(len(cost)):
        cost[i].order = i

    for order in order_list:
        if(order.num==order_can[cost[0].orderfororder].num):
            order_now_num=order.num
            break

    return order_list[order_now_num]


def print_table(path):
    # 显示表格
    fp = open(path, "r")
    table_OrderSku = from_csv(fp)
    print(table_OrderSku)
    fp.close()


def display_order_list(order_list):
    for order in order_list:
        print(order.name,end=',')
    print("(%d)"%len(order_list))
    # print('\n')

def randomcolor():
    colorArr = [
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        'A',
        'B',
        'C',
        'D',
        'E',
        'F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0, 14)]
    return "#" + color