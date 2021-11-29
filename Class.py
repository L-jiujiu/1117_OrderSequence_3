# -*- coding:utf-8 -*-
"""
作者：l_jiujiu
日期：2021.11.17
"""

import pandas as pd
import time as tm
import os
import numpy as np

from prettytable import PrettyTable
from prettytable import from_csv


class Sku:
    def __init__(self, sku_config):
        self.name = sku_config['name']  # sku名称
        self.num = sku_config['num']      # sku序号
        self.sku_time = sku_config['sku_time']  # sku处理所需时间
        self.sku_location_list = sku_config['sku_location_list']  # sku所在分区信息


class Section:
    def __init__(self,section_config):
        self.name=section_config['name']  # 分区名称
        self.num=section_config['num']   # 分区编号（main_1为-1，main_2为-2）

        self.waiting_order_list=[]   # 分区等待处理订单列表，里面存的是订单实例
        self.process_order_list=[]
        self.finish_order_list=[]

        self.max_order_num=section_config['max_order_num']

    # 函数
    def Add_to_waiting_order_list(self,order_now,time):
        # 在section等待订单队列中加入订单
        self.waiting_order_list.append(order_now)
        order_now.now_section_num=self.num
        order_now.time.time_enter_section=time

    def Add_to_finish_order_list(self,order_now,time):
        # 在section完成订单队列中加入订单
        self.finish_order_list.append(order_now)

    def Process_order(self,time):
        # 完成waiting或process中的order：
        if(len(self.process_order_list)==0):#process中无：判断waiting中是否有order
            if(len(self.waiting_order_list)==0):# waiting中无：return 0
                return 0
            else:# waiting中有：waiting[0]加入到process中，order_now=process[0]
                self.process_order_list.append(self.waiting_order_list[0])
                self.waiting_order_list.pop(0)
                self.process_order_list[0].time.time_start_process=time

                self.process_order_list[0].time.cal_period_waiting()
                print('%s'%self.process_order_list[0].name,'在%s'%self.name,'等待用时%d'%self.process_order_list[0].time.period_waiting)
        order_now = self.process_order_list[0]

        # print('工作前%s'%order_now.work_schedule[order_now.now_schedule_num])
        a=int(order_now.work_schedule[order_now.now_schedule_num][1]-1)
        order_now.work_schedule[order_now.now_schedule_num]=(str(self.num),a)
        # print('工作后%s'%order_now.work_schedule[order_now.now_schedule_num])

        # 判断该order_now是否已经完成当前工序，完成则将订单移出process，加入finish
        if(order_now.work_schedule[order_now.now_schedule_num][1]==0):
            self.finish_order_list.append(self.process_order_list[0])
            self.process_order_list.pop(0)
            # print('%s'%self.name,'中%s'%order_now.name,'已完成任务')
            # print('order.now_schedule_num=%s' % order_now.now_schedule_num, end=',')
            # print('len(order.work_schedule)=%s' % len(order_now.work_schedule))

    def Count_num(self):
        a=len(self.waiting_order_list)+len(self.process_order_list)+len(self.finish_order_list)
        return a


class Order:
    def __init__(self, order_config):
        self.name = order_config['name']  # 订单名称
        self.num = order_config['num']  # 订单编号
        self.work_schedule_dic=order_config['work_schedule_dic'] #字典形式存储的作业顺序表

        self.work_schedule=order_config['work_schedule']  #作业顺序表
        self.now_schedule_num=-1  #当前工序对应序号
        self.now_section_num=-1  #当前工序所在section对应序号

        self.time=order_config['time']  #订单处理实时进度
        self.weighted_cost=0

        self.start1not0=0 #初始订单都未被派发

    # 函数
    # 计算订单cost
    def Cost_cal(self,section_list):
        j = 0
        cost=0
        weight=[1,0.8,0.5]
            # print(j)
        for i in range(len(self.work_schedule)):
            if (int(self.work_schedule[i][0]) < 0):  # 如果第i步为mainstream，跳过这一步判断下一步是否还为mainstream
                continue
            else:
                # cost = 1 *（sec0等待队列 + order在sec0处理时间）+0.8 *（sec1等待队列 + order在sec1处理时间）+0.5 *（sec2等待队列 + order在sec2处理时间）
                try:
                    section_waiting_num = len(section_list[int(self.work_schedule[i][0])].waiting_order_list)+len(section_list[int(self.work_schedule[i][0])].process_order_list)+len(section_list[int(self.work_schedule[i][0])].finish_order_list)
                    cost = cost + weight[j] * (int(self.work_schedule[i][1]) + section_waiting_num)
                    # print('section_waiting_num=%d'%section_waiting_num)
                    # print('step_length=%d'%int(work_step[i][1]))
                except:
                    break
                j = j + 1

        self.weighted_cost=cost
        # print("%s" % self.name, "的cost为:%.2f" % self.weighted_cost,"工序为:%s"%self.work_schedule)



class Time:
    def __init__(self,time_config):
        self.order_name=time_config['order_name']  #所属订单名称
        self.now_section_list=time_config['now_section_list']  #经过所在分区名列表
        self.time_enter_section=time_config['time_enter_section']  #进入分区时间
        self.time_start_process=time_config['time_start_process']  #开始拣选时间
        self.time_leave_section=time_config['time_leave_section']  #离开分区时间

        self.period_process=time_config['period_process']  #拣选共计用时
        self.period_waiting=0  #在分区等待共计用时


    # 函数
    # 计算拣选时间
    def cal_period_process(self):
        self.period_process=self.time_leave_section-self.time_start_process+1
    def cal_period_waiting(self):
        self.period_waiting=self.time_start_process-self.time_enter_section

class CostList:
    def __init__(self,cost_config):
        self.name = cost_config['name']
        self.order = cost_config['order']  # 指排序后的顺序，按增序排列
        self.cost = cost_config['cost']
        # 用于删除Order序列中已被分配的订单，记录了原始Order的顺序
        self.orderfororder = cost_config['orderfororder']
