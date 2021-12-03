# -*- coding:utf-8 -*-
"""
作者：l_jiujiu
日期：2021.11.17
"""

# a={'1':1,'2':0,'-1':0}
# k=1
# kk=11
# # a.update(str(k),3)
# a[str(k)]=kk
# # a.pop(str(k))
# # print(a[str(k)])
# print(a)
# # print(list(a.items()[0]))
# print(list(a.items())[2][0])
# # a.append([1,2])
# # num=1
# # num_2=3
# # a.append([num,num_2])
# # print(a[1][0])
# print('sssssss')
# j = 0
# # weight = [1, 0.8, 0.5, 0.3]
#
# while j < 4:
#     # print(weight[j])
#     # print(j)
#     if(j==1):
#         j = j + 1
#         continue
#     else:
#         print(j)
#         # print(weight[j])
#         j = j + 1
#
#     # if(j==2):
#     #     break
#
# a=[]
# a.append((1,1))
# a.append((1,2))
# a[0]=(2,3)


# # print(a)
# i=10
# while(i<3):
#     i=i+1
#     print(i)
#     if(i==2):
#         break
# else:
#     print('111')
#
#
# class A:
#     def __init__(self,A_config):
#         self.name=A_config['name']
#         self.num=A_config['num']
#
# a_input={'name':'a','num':1}
# b_input={'name':'b','num':2}
# c_input={'name':'c','num':3}
#
# alpha=[]
# alpha.append(A(a_input))
# alpha.append(A(b_input))
# alpha.append(A(c_input))
#
# print('origin')
# for a in alpha:
#     print(a.name,end=':')
#     print(a.num)
#
# q=alpha[0]
# q.name='ccc'
# print('change')
# for a in alpha:
#     print(a.name,end=':')
#     print(a.num)
# i=0
# exec("print('{}')".format(i + 1))
#
#

import numpy as np
import pandas as pd

import plotly.graph_objects as go
import plotly.offline as of  	# 这个为离线模式的导入方法

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px


# #
# x_t=[0,3,4,7]
# y_t=[1,10,2,3]
# line1 = go.Scatter(
#     x=x_t,
#     y=y_t,
#     name='<b>No</b> Gaps',  # Style name/legend entry with html tags
#     connectgaps=True
# )
# line2 = go.Scatter(
#     x=x_t,
#     y=y_t,
#     name='Gaps',  # Style name/legend entry with html tags
#     connectgaps=True
# )
# fig = go.Figure([line1,line2])
# fig.update_layout(
#     title = 'New Zealand Weather', #定义生成的plot 的标题
#     xaxis_title = 't',		#定义x坐标名称
#     yaxis_title = '订单数'		#定义y坐标名称
# )
# of.plot(fig)
#
#
# #
# #
# # fig = make_subplots(rows=3,  # 将画布分为两行
# #                         cols=1,  # 将画布分为两列
# #                         subplot_titles=["总产品数",
# #                                         "sku数",
# #                                         "订单数"],  # 子图的标题
# #                         )
# # fig.append_trace(trace=trace, col=1, row=1)
# #
# #
# # fig['layout']['yaxis3'].update(title='平均拣选时间')
# # # fig = go.Figure(data=, layout=layout)
# # # fig.update_layout(title=title,barmode='overlay')
# # fig.update_layout(title='111')
# # # fig.update_traces()
# # of.plot(fig)
#
#

#
# import plotly.graph_objects as go
# import plotly.io as pio
#
# fig = go.Figure(data=[go.Table(header=dict(values=['A column', 'B column']),
#                                cells=dict(values=[[1, 1, 1, 1], [2, 2, 2, 2]]),
#                                )
#                       ]
#                 )
#
# pio.write_image(fig, 'your_file_path.png')


# a=[('0', 0), ('-1', 0), ('3', 0), ('-2', 0)]
# b=[('-1', 0), ('3', 0), ('-2', 0)]
# c=[('-1', 0), ('3', 0), ('-2', 0), ('5', 0)]
# d=[('0', 0), ('-1', 0), ('2', 0), ('-2', 0), ('4', 0)]
#
# list=list[][][]


# list=[]
# list.append([('-1', 0), ('3', 0), ('-2', 0)])
#       # [('-1', 0), ('3', 0), ('-2', 0), ('5', 0)],
#       # [('0', 0), ('-1', 0), ('2', 0), ('-2', 0), ('4', 0)]]
# print(list[0][1][0])
#
# list=[]
# a=[0,1]
# b=[2,3]
# for i in range(len(a)):
#     for j in range(len(b)):
#         list.append([a[i],b[j]])
#
# print(list)

# def dynloop_rcsn(data, cur_y_idx = 0, lst_rst = [], lst_tmp = []):
#     max_y_idx = len(data) - 1  # 获取Y 轴最大索引值
#     for x_idx in range(len(data[cur_y_idx])):  # 遍历当前层的X 轴
#         lst_tmp.append(data[cur_y_idx][x_idx])  # 将当前层X 轴的元素追加到lst_tmp 中
#         if cur_y_idx == max_y_idx:  # 如果当前层是最底层则将lst_tmp 作为元素追加到lst_rst 中
#             lst_rst.append([*lst_tmp])
#         else:  # 如果当前还不是最底层则Y 轴+1 继续往下递归，所以递归最大层数就是Y 轴的最大值
#                # lst_rst 和lst_tmp 的地址也传到下次递归中，这样不论在哪一层中修改的都是同一个list 对象
#             dynloop_rcsn(data, cur_y_idx+1, lst_rst, lst_tmp)
#         lst_tmp.pop()  # 在本次循环最后，不管是递归回来的，还是最底层循环的，都要将lst_tmp 最后一个元素移除
#
#     return lst_rst

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


data = [
    [1, 2],
    # [3, 4, 5],
    # [6, 7, 8, 9]
]
lst_rst=dynloop_loop(data)
print(len(lst_rst))
print(lst_rst)














