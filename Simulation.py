# -*- coding:utf-8 -*-
"""
作者：l_jiujiu
日期：2021.11.17
"""
import operator
import pandas as pd
import time as tm
import os
import numpy as np
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots

import plotly.graph_objects as go
import plotly.offline as of  	# 这个为离线模式的导入方法

from Class import Sku,Section,Order,Time,CostList
from Functions_new1214 import Func_Cost_sequence,Func_Cost_sequence_better,Func_Cost_sequence_better_more,\
    print_table,display_order_list,randomcolor

class Simulation:
    def __init__(self, simulation_config):
        self.T = simulation_config['T']
        self.path_order_sku_map = simulation_config['path_order_sku_map']
        self.path_sku_time_map=simulation_config['path_sku_time_map']

        self.type=simulation_config['type']
        self.pace=simulation_config['pace']

        # 1、初始化section
        self.num_section = simulation_config['num_section']
        self.section_list = []
        # 2、初始化sku
        self.num_sku=0
        self.sku_list = []
        # 3、初始化订单
        self.num_order=0
        self.order_list = []  # order列表
        self.order_notstart = []  # 未发出的order
        self.order_start = []  # 已经开始流转的order
        self.order_finish = []  # 已经流转结束的order
        self.order_before_section=-1

        # 初始化
        self.init_section()
        self.init_sku()
        self.init_order()

        # 画图
        self.x_t = []
        self.y_0 = []
        self.y_0_waiting = []
        self.y_0_process = []

        self.y_1 = []
        self.y_1_waiting = []
        self.y_1_process = []

        self.y_2 = []
        self.y_2_waiting = []
        self.y_2_process = []

        self.y_3 = []
        self.y_3_waiting = []
        self.y_3_process = []

        self.y_4 = []
        self.y_4_waiting = []
        self.y_4_process = []

        self.y_5 = []
        self.y_5_waiting = []
        self.y_5_process = []

        self.y_11 = []
        self.y_22 = []

        self.fig = plt.figure()

        self.main_jam_1=0 #主路的拥堵情况
        self.main_jam_2=0 #主路的拥堵情况


    def init_section(self):
        # 初始化6个section信息：分区名称、正在等待的订单数量、处理订单列表
        print('所有Section个数为：%d' % self.num_section,'主干道中转站个数为：2')
        for i in range(0,(self.num_section),1):
            section_input = {
                'name': str(i+17)+'01',  # 分区名称
                'num': i,  # 分区序号
                'max_order_num':6  #最多停滞order数量
            }
            self.section_list.append(Section(section_input))

        for j in range(-2,0,1):
            # print(j)
            section_input = {
                'name': 'section_{}'.format(j),  # 分区名称
                'num': j,  # 分区序号
                'max_order_num': 1  # 最多停滞order数量

            }
            self.section_list.append(Section(section_input))
        # 显示当前section命名方式，可以用section_list[-1]调用第一个mainstream节点，-2调用第二个
        # for section in self.section_list:
        #     print(section.name)
        # 测试数据
        # print('section_list[-2]=%d'%self.section_list[-2].num)

        # self.section_list[-1].waiting_order_list=[1,1]
        # self.section_list[3].waiting_order_list=[1,1,1,1,1,1,1]

    def init_sku(self):
        # 初始化sku所在的分区：sku名称，sku处理所需时间、sku所在分区
        df = pd.read_excel(self.path_sku_time_map, sheet_name='Part 1', usecols='C,E')
        df.dropna(axis=0, how='any', inplace=True)
        data = df.values
        self.num_sku = len(data)
        print('所有Sku数量为：%d ' % self.num_sku)

        for i in range(0, self.num_sku):
            sku_input={
                'name': str(int(data[i][0])),  # sku名称
                'num': i,  # sku序号
                'sku_time': data[i][1],  # sku处理所需时间（默认为1）
            }
            self.sku_list.append(Sku(sku_input))
        # 显示表格
        # for sku in self.sku_list:
            # print('%s'%sku.name+",%d"%sku.num,',%d'%sku.sku_time)

    def init_order(self):
        data = pd.read_excel(self.path_order_sku_map, sheet_name='Part 1', usecols='A,B,C,D',
                             names=['OrderID', 'CommodityID', 'Amount', 'PosGroupID'])
        data.dropna(axis=0, how='any', inplace=True)
        order_num = data['PosGroupID'].groupby(data['OrderID']).count()
        self.num_order=order_num.size

        for i in range(0,self.num_order):
            order_name=str(order_num.index[i])
            order_data = data.loc[data['OrderID'] == order_num.index[i], ['PosGroupID', 'Amount']]
            # print(order_data)

            result_data = order_data['Amount'].groupby(data['PosGroupID']).sum()
            work_schedule_origin = []
            for g in range(len(list(result_data.index))):
                work_schedule_origin.append([list(result_data.index)[g], list(result_data.values)[g]])
            # print(work_schedule_origin)

            #在work_schedule中加入主干道的信息
            work_schedule_dic = {'0': 0, '1': 0, '-1': 0, '2': 0, '3': 0, '-2': 0, '4': 0, '5': 0}
            for p in range(len(work_schedule_origin)):
                key_num=int(int(work_schedule_origin[p][0])/100)-17
                work_schedule_dic[str(key_num)] = work_schedule_origin[p][1]
            for i in range(6):
                if (work_schedule_dic[str(i)] == 0):
                    work_schedule_dic.pop(str(i))

            # work_schedule_dic = {'1701': 0, '1801': 0, '-1': 0, '1901': 0, '2001': 0, '-2': 0, '2101': 0,'2201': 0}
            # for p in range(len(work_schedule_origin)):
            #     work_schedule_dic[str(work_schedule_origin[p][0])] = work_schedule_origin[p][1]
            # for i in range(6):  # 去除无工作的分区
            #     if (work_schedule_dic[str(i + 17) + '01'] == 0):
            #         work_schedule_dic.pop(str(i + 17) + '01')

            work_schedule = [[k, v] for k, v in work_schedule_dic.items()]  # 将字典转化为列表
            # print('[%s'%order_name,']work_schedule:%s'%work_schedule)

            time_input = {'order_name':order_name ,
                          'now_section_list': [],
                          'time_enter_section': 0,
                          'time_start_process': 0,
                          'period_process': 0,
                          'time_leave_section': 0}

            order_input = {'name': order_name,  # 订单名称
                           'num': i,  # 订单序号
                           'work_schedule': work_schedule,
                           'time': Time(time_input)}
            self.order_list.append(Order(order_input))
            self.order_notstart.append(Order(order_input))
        print('所有Order数量为：%d ' % self.num_order)
        simple_num=0
        for order in self.order_notstart:
            if(len(order.work_schedule)==3):
                simple_num=simple_num+1
        print('simple_num=%d'%simple_num,',比例为:%.3f'%(simple_num/self.num_order))


    def Func_Order_filter(self):
        order_fluent = []  # 筛选在mainstream上可以不堵的订单
        order_can = []  # 进而筛选在section中排队次数小于6次的订单
        for order in self.order_notstart:
            # work_step[i][j]：[i]对应第i步；[j=0]对应section名，[j=1]对应工序用时
            work_step = order.work_schedule

            if (int(work_step[0][0]) >= 0):  # 如果第0步不为mainstream，可以
                order_fluent.append(order)
            else:
                if (len(self.section_list[int(work_step[0][0])].waiting_order_list)+len(self.section_list[int(work_step[0][0])].finish_order_list) == 0):  # 如果第0步为mainstream，并且第0步等待数量为0，
                    if (int(work_step[1][0]) >= 0):  # 如果第1步不为mainstream，则可以
                        order_fluent.append(order)
                    else:  # 如果第1步为mainstream，则继续判断第1步等待数量
                        if (len(self.section_list[int(work_step[1][0])].waiting_order_list) + len(self.section_list[int(
                                work_step[1][0])].finish_order_list) == 0):  # 如果第1步等待数量为0，则可以，否则不可以
                            order_fluent.append(order)
        print('order_fluent%d:'%len(order_fluent), end='')
        display_order_list(order_fluent)

        for order_2 in order_fluent:
            work_step = order_2.work_schedule
            for i in range(len(work_step)):
                if (int(work_step[i][0]) < 0):  # 如果第i步为mainstream，跳过这一步判断下一步是否还为mainstream
                    continue
                else:
                    all_order_num=len(self.section_list[int(work_step[i][0])].waiting_order_list)+len(self.section_list[int(work_step[i][0])].process_order_list)+len(self.section_list[int(work_step[i][0])].finish_order_list)
                    if (all_order_num < 6):  # 找到第一步不是mainstream的判断，如果第i步的等待数量小于6，则可以被派发
                        order_can.append(order_2)
                        break
                    else:
                        break
        # print('order_can:', end='')
        # display_order_list(order_can)
        return order_can,order_fluent

    def Find_Section_now_num(self,order_now):
        # section_now为第一个不为负的section
        for i in range(len(order_now.work_schedule)):
            if (int(order_now.work_schedule[i][0]) < 0):  # 如果第i步为mainstream，跳过这一步判断下一步是否还为mainstream
                continue
            else:
                section_now_num = int(order_now.work_schedule[i][0])
                schedule_now_num = i
                break
        return section_now_num,schedule_now_num

    # 新测试的代码
    def Func_Assign_Order(self,time):
        # 1\过滤可能有堵塞问题的订单
        order_can, order_fluent = self.Func_Order_filter()

        # 2\按照cost选出影响最小的订单,赋予order_now
        if (len(order_can) > 0):
            # 求出最小cost订单对应的序号（它在order_list中的顺序就是他的num）
            # 所以self.order_list[order_now_num]就是被选派的订单

            # order_now = Func_Cost_sequence(order_can, self.section_list,self.order_list,self.order_before_section)
            # order_now = Func_Cost_sequence_better(order_can, self.section_list,self.order_list,self.order_before_section)
            order_now = Func_Cost_sequence_better_more(order_can, self.section_list,self.order_list,self.order_before_section)

        else:
            if (len(order_fluent) != 0):
                print("section已满，本轮无订单被派发")
            else:
                print("主干道堵塞，本轮无订单被派发")
            return 0

        # 3\赋予section_now为order_now第一个不为负的section，得到第一个不为负section的编号和当前order所处的工序
        order_now.now_section_num,order_now.now_schedule_num=self.Find_Section_now_num(order_now)
        print('当前派发的订单为%s'%order_now.name,',地点为%s'%self.section_list[order_now.now_section_num].name,"对应工序序号为%d"%order_now.now_schedule_num,'工序为:%s'%order_now.work_schedule)

        # 4\在section等待队列中加入订单信息(订单序号，订单在该区用时)
        self.section_list[order_now.now_section_num].Add_to_waiting_order_list(order_now,time)
        #更新order_before_section：上一个派发订单第一个取得非主路section
        self.order_before_section=order_now.now_section_num

        # 5\修改订单信息
        # time_enter_section记录
        order_now.time.time_enter_section=time

        # 6\在未发出订单信息中删除order_now
        for i in range(len(self.order_notstart)):
            if (self.order_notstart[i].name == order_now.name):
                self.order_start.append(self.order_notstart[i])
                self.order_notstart.pop(i)
                break

    # 新旧代码简单粗暴的结合
    # def Func_Assign_Order(self, time):
    #     # 1\过滤可能有堵塞问题的订单
    #     order_can, order_fluent = self.Func_Order_filter()
    #
    #     key = 0
    #     if (len(order_can) > 0):
    #         # 求出只有一个section要去的，并且该section的waiting+process为空的订单
    #         for order in order_can:
    #             if (len(order.work_schedule) == 3):
    #                 section_now_num, schedule_now_num = self.Find_Section_now_num(order)
    #                 section_temp = self.section_list[section_now_num]
    #                 section_waiting_num = len(section_temp.waiting_order_list) + len(
    #                     section_temp.process_order_list) + len(section_temp.finish_order_list)
    #                 if (section_waiting_num == 0):
    #                     order_now = order
    #                     key = 1
    #                     break
    #         if (key == 0):
    #             order_now = Func_Cost_sequence_better(order_can, self.section_list, self.order_list,
    #                                                   self.order_before_section)
    #             # order_now = order_can[0]
    #
    #     else:
    #         if (len(order_fluent) != 0):
    #             print("section已满，本轮无订单被派发")
    #         else:
    #             print("主干道堵塞，本轮无订单被派发")
    #         return 0
    #
    #     # 3\赋予section_now为order_now第一个不为负的section，得到第一个不为负section的编号和当前order所处的工序
    #     order_now.now_section_num, order_now.now_schedule_num = self.Find_Section_now_num(order_now)
    #     print('当前派发的订单为%s' % order_now.name, ',地点为%s' % self.section_list[order_now.now_section_num].name,
    #           "对应工序序号为%d" % order_now.now_schedule_num, '工序为:%s' % order_now.work_schedule)
    #
    #     # 4\在section等待队列中加入订单信息(订单序号，订单在该区用时)
    #     self.section_list[order_now.now_section_num].Add_to_waiting_order_list(order_now, time)
    #     # 更新order_before_section：上一个派发订单第一个取得非主路section
    #     self.order_before_section = order_now.now_section_num
    #
    #     # 5\修改订单信息
    #     # time_enter_section记录
    #     order_now.time.time_enter_section = time
    #
    #     # 6\在未发出订单信息中删除order_now
    #     for i in range(len(self.order_notstart)):
    #         if (self.order_notstart[i].name == order_now.name):
    #             self.order_start.append(self.order_notstart[i])
    #             self.order_notstart.pop(i)
    #             break
    # 发网原始算法
    def Func_Assign_Order_Origin(self,time):
        # 1\过滤可能有堵塞问题的订单
        order_can, order_fluent = self.Func_Order_filter()
        # 2\按照cost选出影响最小的订单,赋予order_now
        key=0
        if (len(order_can) > 0):
            # 求出只有一个section要去的，并且该section的waiting+process为空的订单
            for order in order_can:
                if(len(order.work_schedule)==3):
                    section_now_num, schedule_now_num=self.Find_Section_now_num(order)
                    section_temp=self.section_list[section_now_num]
                    section_waiting_num = len(section_temp.waiting_order_list)+len(section_temp.process_order_list)+len(section_temp.finish_order_list)
                    if(section_waiting_num==0):
                        order_now=order
                        key=1
                        break
            if (key == 0):
                order_now = order_can[0]

        else:
            if (len(order_fluent) != 0):
                print("section已满，本轮无订单被派发")
            else:
                print("主干道堵塞，本轮无订单被派发")
            return 0

        # 3\赋予section_now为order_now第一个不为负的section，得到第一个不为负section的编号和当前order所处的工序
        order_now.now_section_num,order_now.now_schedule_num=self.Find_Section_now_num(order_now)
        print('当前派发的订单为%s'%order_now.name,',地点为%s'%self.section_list[order_now.now_section_num].name,"对应工序序号为%d"%order_now.now_schedule_num,'工序为:%s'%order_now.work_schedule)

        # 4\在section等待队列中加入订单信息(订单序号，订单在该区用时)
        self.section_list[order_now.now_section_num].Add_to_waiting_order_list(order_now,time)

        # 5\修改订单信息
        # time_enter_section记录
        order_now.time.time_enter_section=time

        # 6\在未发出订单信息中删除order_now
        for i in range(len(self.order_notstart)):
            if (self.order_notstart[i].name == order_now.name):
                self.order_start.append(self.order_notstart[i])
                self.order_notstart.pop(i)
                break

    def display_order_list_section(self,i):
        print("%s" % self.section_list[i].name, "的process", end=':')
        for order in self.section_list[i].process_order_list:
            print(order.name, end=',')
        print("(%d)" % len(self.section_list[i].process_order_list), end=';')

        print("     waiting", end=':')
        for order in self.section_list[i].waiting_order_list:
            print(order.name, end=',')
        print("(%d)" % len(self.section_list[i].waiting_order_list), end=';')

        print("     finish", end=':')
        for order in self.section_list[i].finish_order_list:
            print(order.name, end=',')
        print("(%d)" % len(self.section_list[i].finish_order_list))

    def display_order_list_mainsec(self):
        list_test=[0,1,-1,2,3,-2,4,5]
        for list_num in list_test:
            if(list_num>=0):
                self.display_order_list_section(list_num)
            else:
                print("     %s" % self.section_list[list_num].name, "的finish", end=':')

                for order in self.section_list[list_num].finish_order_list:
                    print(order.name, end=',')
                print("(%d)" % len(self.section_list[list_num].finish_order_list))

    def display_order_list_all_section(self):
        for i in range(0, 6):
            print("%s" % self.section_list[i].name, "的process", end=':')
            for order in self.section_list[i].process_order_list:
                print(order.name, end=',')
            print("(%d)" % len(self.section_list[i].process_order_list),end=';')

            print("     waiting", end=':')
            for order in self.section_list[i].waiting_order_list:
                print(order.name, end=',')
            print("(%d)" % len(self.section_list[i].waiting_order_list),end=';')

            print("     finish", end=':')
            for order in self.section_list[i].finish_order_list:
                print(order.name, end=',')
            print("(%d)" % len(self.section_list[i].finish_order_list))

    def move_to_next_schedule(self,order_now, section_list,time):
        while (int(order_now.now_schedule_num) + 1 < len(order_now.work_schedule)):
            # print('order.now_schedule_num=%s' % self.now_schedule_num, end=',')
            # print('len(order.work_schedule)=%s' % len(self.work_schedule))
            section_now = section_list[int(order_now.work_schedule[order_now.now_schedule_num][0])]
            section_next = section_list[int(order_now.work_schedule[order_now.now_schedule_num + 1][0])]
            if ((len(section_next.waiting_order_list) + len(section_next.process_order_list) + len(
                    section_next.finish_order_list)) >= section_next.max_order_num):
                # 堵了：now_schedule_num不变，将order加入到now_schedule_num的finish_list中，break
                section_list[int(order_now.work_schedule[order_now.now_schedule_num][0])].Add_to_finish_order_list(order_now,time+1)
                break
            else:
                # 不堵：看now_schedule_num + 1是main还是section
                if(section_next.num<0): #是main
                    order_now.now_schedule_num=order_now.now_schedule_num+1
                else: #是section
                    order_now.now_schedule_num=order_now.now_schedule_num+1
                    section_list[int(order_now.work_schedule[order_now.now_schedule_num][0])].Add_to_waiting_order_list(order_now,time+1)
                    break
        else:
            return 0
        return 1


    def plot_scatter(self,y,title,key):
        color = {
            'all': ['circle','blue'],
            'waiting': ['circle-open','orange'],
            'process': ['square','green'],
        }

        section_all = go.Scatter(
            x=self.x_t,
            y=y,
            name=title,  # Style name/legend entry with html tags
            connectgaps=True,
            marker=dict(symbol=color[key][0], color=color[key][1]),
        )

        return section_all

    def plot_results_plotly(self):
        # 用plotly画图
        fig = make_subplots(
            rows=8, cols=1,
            subplot_titles=("section_<b>0</b>",
                             "section_<b>1</b>",
                             "section_<b>2</b>",
                             "section_<b>3</b>",
                             "section_<b>4</b>",
                             "section_<b>5</b>",
                            "section_<b>-1</b>",
                            "section_<b>-2</b>",
                             )
        )
        list_test = [0, 1, -1, 2, 3, -2, 4, 5]
        for i in list_test:
            if(i==-1):
                fig.add_trace(self.plot_scatter(self.y_11, 'section_<b>%d</b> all' % i,key='all'), row = 7, col = 1)
            elif(i==-2):
                fig.add_trace(self.plot_scatter(self.y_22, 'section_<b>%d</b> all' % i,key='all'), row = 8, col = 1)
            else:
                # print('1')
                exec("fig.add_trace(self.plot_scatter(self.y_{},'section_<b>%d</b> all'%{},key='all'),row=i+1,col=1)".format(i,i))
                # exec("fig.add_trace(self.plot_scatter(self.y_{}_waiting, 'section_<b>%d</b> waiting' % {},key='waiting'), row=i + 1, col=1)".format(i,i))
                # exec("fig.add_trace(self.plot_scatter(self.y_{}_process, 'section_<b>%d</b> process' % {},key='process'), row=i + 1, col=1)".format(i,i))

        layout = go.Layout(title='各时段分区订单累积情况',  # 定义生成的plot 的标题
            # xaxis_title='时间',  # 定义x坐标名称
            yaxis_title='订单数',  # 定义y坐标名称
                           )
        fig.update_layout(layout)
        of.plot(fig,filename = 'your_file_path.html')

    def plot_results(self):
        # 用matplot画图
        for i in range(len(self.section_list)):
            section_now=self.section_list[i]
            if (section_now.num == -1):
                ax = self.fig.add_subplot(8, 1, 7)
                plt.title('section_-1', fontsize=10)
                ax.plot(self.x_t, self.y_11, color=randomcolor(), linewidth=2)
            elif (section_now.num == -2):
                ax = self.fig.add_subplot(8, 1, 8)
                plt.title('section_-2', fontsize=10)
                ax.plot(self.x_t, self.y_22, color=randomcolor(), linewidth=2)
            else:
                ax = self.fig.add_subplot(8,1,(i+1))
                exec("plt.title('$section{}$', fontsize=10)".format(i))
                exec("ax.plot(self.x_t, self.y_{}, color=randomcolor(), linewidth=2)".format(i))
            i=i+1
        plt.show()


    def save_y_t(self):
        for i in range(len(self.section_list)):
            a = self.section_list[i].Count_num()
            if (self.section_list[i].num == -1):
                self.y_11.append(a)
            elif (self.section_list[i].num == -2):
                self.y_22.append(a)
            else:
                exec("self.y_{}.append(a)".format(i))
                exec("self.y_{}_waiting.append(len(self.section_list[i].waiting_order_list))".format(i))
                exec("self.y_{}_process.append(len(self.section_list[i].process_order_list))".format(i))

    def run(self):
        for t in range(1,self.T):

            print("\n")
            print(
                "--------------------------\n     当前时刻为%d\n--------------------------" %
                t)

        # step1：下发新的订单
            if((t+1)%self.pace==0):
                if(len(self.order_notstart)!=0):
                    if(self.type=='new'):
                        self.Func_Assign_Order(time=t)
                    elif (self.type == 'origin'):
                        self.Func_Assign_Order_Origin(time=t)
                else:
                    print('*********无order可派发*********\n')

            # 画图
            self.x_t.append(t)
            self.save_y_t()

            print('各section初始情况：')
            self.display_order_list_mainsec()
            # self.display_order_list_all_section()

        # step2：对每个section进行正序遍历，依次完成当前section中的任务
            print('\n*********对各section中订单进行遍历，依次完成*********')
            for i in range(0, 6):
                self.section_list[i].Process_order(time=t)

            # print('各section完成初始订单后：')
            # self.display_order_list_all_section()

        # step3：对每个section+mainstream进行倒序遍历，依次对section中finish的订单进行移动
            list_test = [5, 4, -2, 3, 2, -1, 1, 0]
            for list_num in list_test:
                section_now = self.section_list[list_num]
                count=len(section_now.finish_order_list)
                while(count>0):
                    order_now=section_now.finish_order_list[0]
                    section_now.finish_order_list.pop(0)
                    count=count-1
                    # print('%s'%section_now.name,'中的%s'%order_now.name,'移动')

                    key=self.move_to_next_schedule(order_now=order_now, section_list=self.section_list,time=t)
                    if(key==0):
                        print('%s' % order_now.name, '已完成全部任务')
                        self.order_finish.append(order_now)

            # 显示
            print('\nt=%d' % t, '时刻结束：', end='\n')
            self.display_order_list_mainsec()
            print('\norder_start%d:'%len(self.order_start), end='')
            display_order_list(self.order_start)
            print('order_finish%d:'%len(self.order_finish), end='')
            display_order_list(self.order_finish)

            # 记录主路堵车次数
            if(len(self.section_list[7].finish_order_list)!=0):
                self.main_jam_1 =self.main_jam_1+1   # 主路的拥堵情况
            if (len(self.section_list[6].finish_order_list) != 0):
                self.main_jam_2 = self.main_jam_2 + 1  # 主路的拥堵情况

            # # 画图
            # self.x_t.append(t)
            # self.save_y_t()

            # 订单全部完成，退出循环
            if (len(self.order_finish) == self.num_order):
                T_last = t
                break


        print('[Order：%d ' % self.num_order,'Sku：%d]' % self.num_sku,',%s'%self.type)
        print('完成全部订单共计循环次数：%d' % T_last)
        print('主路-1拥堵情况：%d' % self.main_jam_1,'主路-2拥堵情况：%d' % self.main_jam_2)

        # for order in self.order_list:
        #     print(order.work_schedule)

if __name__ == "__main__":
    start = tm.perf_counter()  # 记录当前时刻
    cwd = os.getcwd()  # 读取当前文件夹路径


    simulation_config = {
        'T': 5000000000,  # 仿真时长
        'num_section': 6,

        'type':'new',
        # 'type':'origin',
        'pace':1,

        # # 初始数据
        'path_order_sku_map': cwd + '/Fa_data/OrderPickDetail.xlsx',
        # 'path_order_sku_map': cwd + '/Fa_data/OrderPickDetail_less.xlsx',
        'path_sku_time_map': cwd + '/Fa_data/PickLinePos_time.xlsx',

    }
    simulation_1 = Simulation(simulation_config)

    simulation_1.run()
    end = tm.perf_counter()
    print("程序共计用时 : %s Seconds " % (end - start))

    simulation_1.plot_results_plotly()


