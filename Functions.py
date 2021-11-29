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
                order_section_time = order_section_time + sku_list[order_sku_num_list[num]].sku_time * order_sku_number_list[num]

        work_schedule[str(section.num)]=order_section_time

    for i in range(6):
        if (work_schedule[str(i)]==0):
            work_schedule.pop(str(i))
    print(work_schedule)
    return work_schedule

def dynloop_rcsn(data, cur_y_idx = 0, lst_rst = [], lst_tmp = []):
    max_y_idx = len(data) - 1  # 获取Y 轴最大索引值
    for x_idx in range(len(data[cur_y_idx])):  # 遍历当前层的X 轴
        lst_tmp.append(data[cur_y_idx][x_idx])  # 将当前层X 轴的元素追加到lst_tmp 中
        if cur_y_idx == max_y_idx:  # 如果当前层是最底层则将lst_tmp 作为元素追加到lst_rst 中
            lst_rst.append([*lst_tmp])
        else:  # 如果当前还不是最底层则Y 轴+1 继续往下递归，所以递归最大层数就是Y 轴的最大值
               # lst_rst 和lst_tmp 的地址也传到下次递归中，这样不论在哪一层中修改的都是同一个list 对象
            dynloop_rcsn(data, cur_y_idx+1, lst_rst, lst_tmp)
        lst_tmp.pop()  # 在本次循环最后，不管是递归回来的，还是最底层循环的，都要将lst_tmp 最后一个元素移除

    return lst_rst
def dynloop_loop(data):
    # 变量初始化
    max_y_idx = len(data)  # 获取原2 维数组Y 轴最大值
    row_max_idx = 1  # 记录X 轴的最大值，初始为1，下面会计算
    arr_len, lst_row, lst_rst = [], [], []
    arr_idx = [0] * max_y_idx  # 保存每次提取max_y_idx 个元素的索引值的集合，初始值为[0, 0, 0, 0]

    # 将2 维数组data 转换成1 维数组lst_row
    for item in data:
        _n = len(item)  # 求原2 维数组中每一层的长度
        arr_len.append(_n)  # 保存原2 维数组中每一层的长度的集合
        lst_row += item  # 将原2 维数组的每个元素累加到1 维数组lst_row 中
        row_max_idx *= _n  # 记录1 维数组需要循环的总数

    # 遍历1 维数组
    for row_idx in range(row_max_idx):
        # 求每个被提取的元素的索引值
        for y_idx in range(max_y_idx):
            # 遍历原2 维数组各层长度的'切片'集合，例如：lst = [1, 2, 3, 4]
            # 则lst[2:] 为[3, 4] 即从下标2 开始后面全要；lst[:2] 为[1, 2] 即到下标2 之前都要
            # _pdt 是product 乘积的缩写，记录原2 维数组当前层之下所有层长度的乘积
            _pdt = 1
            for n in arr_len[y_idx+1:]:
                _pdt *= n
            # _offset 是偏移量，记录原2 维数组当前层之上所有层长度的和
            _offset = 0
            for n in arr_len[:y_idx]:
                _offset += n
            # 计算元素提取索引：当前X 轴的值除以_pdt，再与原2 维数组当前层长度取余，最后加上偏移量
            arr_idx[y_idx] = (row_idx // _pdt) % arr_len[y_idx] + _offset

        # 遍历索引集合，从1 维数组中提选元素放入_lst_tmp 中
        _lst_tmp = []
        for idx in arr_idx:
            _lst_tmp.append(lst_row[idx])
        # 最后将_lst_tmp 作为元素追加到lst_rst 中
        lst_rst.append(_lst_tmp)

    return lst_rst

def Func_ReadCsv_SkuOrder_new(i,num_sku,data,section_list,sku_list):
    order_sku_num_list = []  # order中含有的sku的序号
    order_sku_number_list = []  # order中各sku序号对应的数量
    order_sku_section_list=[] #order中各sku所在分区名称，对于多种情况则有多个列表
    work_schedule_list=[]
    temp = []  # 用于临时存放第i行ordersku列表中不为0的列，即对应的sku信息

    # 读取所有数据，统计为1的列目标是在该分区
    for z in range(0, num_sku):
        temp.append(data[i + 1, z + 1])
        if (temp[z] != 0):
            order_sku_num_list.append(z)
            order_sku_number_list.append(temp[z])

    for num in range(len(order_sku_num_list)):
        order_sku_section=[]
        # order_sku_section_list_all=[]

        for section in sku_list[order_sku_num_list[num]].sku_location_list:
            order_sku_section.append(section.name)
        order_sku_section_list.append(order_sku_section)

    print('order_sku_section_list: %s'%order_sku_section_list)
    order_sku_section_list_all=dynloop_loop(order_sku_section_list)
    print('order_sku_section_list_all: %s'%order_sku_section_list_all)
    print(len(order_sku_section_list_all))
    for all_i in range(len(order_sku_section_list_all)):
        work_schedule = {'0':0,'1':0,'-1':0,'2':0,'3':0,'-2':0,'4':0,'5':0}
    # 将分区信息记录在sku对应分区的列表中
        for section in section_list:
            order_section_time = 0
            for num in range(len(order_sku_num_list)):
                if (order_sku_section_list_all[all_i][num] == section.name):
                    order_section_time = order_section_time + sku_list[order_sku_num_list[num]].sku_time * order_sku_number_list[num]

            work_schedule[str(section.num)]=order_section_time

        for i in range(6):
            if (work_schedule[str(i)]==0):
                work_schedule.pop(str(i))

        work_schedule_list.append(work_schedule)
    for j in range(len(work_schedule_list)):
        print('work_schedule%d'%j)
        print(work_schedule_list[j])
    print(work_schedule_list)
        # 两个section只能去一个！
    return work_schedule

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
        section_all_num=section_all_num+len(section.finish_order_list)+len(section.waiting_order_list)+len(section.process_order_list)

    if(section_all_num==0):
        print('系统很闲！')
        for order in order_list:
            if (order.num == order_can[cost[-1].orderfororder].num):
                order_now_num = order.num
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

    # 优化1：
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
            if (order.num == order_min.num):
                order_now_num = order.num
                break

    # for order in order_list:
    #     if(order.num==order_can[cost[0].orderfororder].num):
    #         order_now_num=order.num
    #         break
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