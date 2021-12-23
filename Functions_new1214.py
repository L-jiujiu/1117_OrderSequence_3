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
def Find_Section_now_num(order_now):
    # section_now为第一个不为负的section
    for i in range(len(order_now.work_schedule)):
        if (int(order_now.work_schedule[i][0]) < 0):  # 如果第i步为mainstream，跳过这一步判断下一步是否还为mainstream
            continue
        else:
            section_now_num = int(order_now.work_schedule[i][0])
            schedule_now_num = i
            break
    return section_now_num,schedule_now_num

def Func_Cost_sequence(order_can,section_list,order_list,order_before_section):
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



def Func_Cost_sequence_tool(order_min_can):
    # 优化1：把相同cost中比较复杂的订单先发:
    order_min = order_min_can[0]
    for order in order_min_can:
        if (len(order.work_schedule) > len(order_min.work_schedule)):
            order_min = order

    return order_min

def Func_Cost_sequence_better(order_can,section_list,order_list,order_before_section):
    cost = []
    order_min_can=[] #cost相同的订单集合，从中选择最小
    order_min_can_can = []
    order_return=None
    # print('11111')
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

# 优化3：很闲的时候(所有section无订单)，先做最复杂的
    section_all_num=0
    for section in section_list:
        # 1\很闲时所有类型订单为空
        section_all_num=section_all_num+len(section.finish_order_list)+len(section.waiting_order_list)+len(section.process_order_list)
        # 2\(效果更好)很闲时所有订单只有waiting订单为空
        # section_all_num=section_all_num+len(section.waiting_order_list)
    if(section_all_num==0):
        print('系统很闲！')
        for order in order_list:
            if (order.name == order_can[cost[-1].orderfororder].name):
                order_return=order
                break
    else:
        print('系统不闲！')

        cost_min=cost[0].cost
        for order in order_can:
            if(order.weighted_cost==cost_min):
                order_min_can.append(order)
    # 优化2：过滤与上一个派发order第一个去的section不同的单子
        for order in order_min_can:
            section_now_num, schedule_now_num=Find_Section_now_num(order)
            if(section_now_num!=order_before_section):
                order_min_can_can.append(order)
    # 优化1：相同Cost时优先派发复杂订单（经停分区多）
        if(len(order_min_can_can)==0):
            # print(order_min_can)
            print('所有派发的单子第一个section都相同')
            print('order_before_section:%d'%order_before_section)
            order_min=Func_Cost_sequence_tool(order_min_can)
        else:
            # print(order_min_can_can)
            print('order_before_section:%d'%order_before_section)
            order_min=Func_Cost_sequence_tool(order_min_can_can)

        for order in order_list:
            if (order.name == order_min.name):
                order_return=order
                break

    return order_return

def Func_Cost_sequence_better_more(order_can,section_list,order_list,order_before_section):
    cost = []
    order_min_can=[] #cost相同的订单集合，从中选择最小
    order_min_can_can = []
    order_return=None
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

# 优化：对于非上一时刻派发了工作，并且当前没有工作的section，优先派发在这个分区工作时间最长的订单；
    # 如果所有section都有工作，则派发整体cost最小的订单；
    # 还可以测试一下如果所有都无事先派发cost最大会不会有好处。

    section_all_num=0
    for section in section_list:
        # 1\很闲时所有类型订单为空
        section_all_num=section_all_num+len(section.finish_order_list)+len(section.waiting_order_list)+len(section.process_order_list)
        # 2\(效果更好)很闲时所有订单只有waiting订单为空
        # section_all_num=section_all_num+len(section.waiting_order_list)
    if(section_all_num==0):
        print('系统很闲！')
        for order in order_list:
            if (order.name == order_can[cost[-1].orderfororder].name):
                order_return=order
                break
    else:
        print('系统不闲！')
        section_can=[]
        order_light_can=[]

        for section in section_list:
            # 和上一个派发工作的section不同
            if(section.num==order_before_section):
                continue

            section_all=len(section.finish_order_list) + len(section.waiting_order_list) + len(section.process_order_list)
            if(section_all==0):
                section_can.append(section)

        if(len(section_can)!=0):
            for section in section_can:
                print(section.name)
                for order in order_can:
                    section_now_num, schedule_now_num=Find_Section_now_num(order)
                    if(section_now_num==section.num):
                        order_light_can.append(order)

        if(len(order_light_can)!=0):
            order_return=order_light_can[0]
            section_now_num, schedule_now_num = Find_Section_now_num(order_light_can[0])
            schedule_max=order_return.work_schedule[schedule_now_num][1]
            # print('!!!order_return.work_schedule[schedule_now_num][1]=%d' % order_return.work_schedule[schedule_now_num][1])

            for order in order_light_can:
                section_now_num, schedule_now_num = Find_Section_now_num(order)
                if(order.work_schedule[schedule_now_num][1]>schedule_max):
                    schedule_max=order.work_schedule[schedule_now_num][1]
                    order_return=order
                    # print('!!!order.work_schedule[schedule_now_num][1]=%d'%order_return.work_schedule[schedule_now_num][1])

        elif(len(order_light_can)==0):
            cost_min=cost[0].cost
            for order in order_can:
                if(order.weighted_cost==cost_min):
                    order_min_can.append(order)
        # 优化2：过滤与上一个派发order第一个去的section不同的单子
            for order in order_min_can:
                section_now_num, schedule_now_num=Find_Section_now_num(order)
                if(section_now_num!=order_before_section):
                    order_min_can_can.append(order)
        # 优化1：相同Cost时优先派发复杂订单（经停分区多）
            if(len(order_min_can_can)==0):
                # print(order_min_can)
                print('所有派发的单子第一个section都相同')
                print('order_before_section:%d'%order_before_section)
                order_min=Func_Cost_sequence_tool(order_min_can)
            else:
                # print(order_min_can_can)
                print('order_before_section:%d'%order_before_section)
                order_min=Func_Cost_sequence_tool(order_min_can_can)

            for order in order_list:
                if (order.name == order_min.name):
                    order_return=order
                    break

    return order_return
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