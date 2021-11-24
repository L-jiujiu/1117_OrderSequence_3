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


import plotly.graph_objects as go
import plotly.io as pio

fig = go.Figure(data=[go.Table(header=dict(values=['A column', 'B column']),
                               cells=dict(values=[[1, 1, 1, 1], [2, 2, 2, 2]]),
                               )
                      ]
                )

pio.write_image(fig, 'your_file_path.png')



























