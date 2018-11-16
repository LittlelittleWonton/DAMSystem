#!/usr/bin/env python
#-*-coding:utf-8-*-
import datetime
from util.samplerange import Samplerange
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import copy
from matplotlib import font_manager as fm
from matplotlib import  cm
import numpy as np
import os
import logging

#logger = logging.getLogger('scripts')
matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus']=False     # 正常显示负号

def line_kinds():
    color = random.choice([r'b',r'c',r'g' , r'k' , r'm' , r'r',r'y' , r'c'  ])
    style = random.choice([r'.',r',',r'o',r'v' , r'^',r'<',r'>',r'1',r'2',r'3',r'4',r's',r'p',r'*',r'h',r'H',r'd',r'|',r'_',r'+',r'x'])
    kind = random.choice([r'-',r'--',r'-.',r':'])
    return color+style+kind

def draw_plot(xn_dict,calllist):
    '''
    绘制折线图
    :param xn_dict:
    :return:
    '''
    try:
        legend = [ k['label'] for k in xn_dict['y']['ylist']]
        group_labels=xn_dict['group_labels']
        title = xn_dict['title']
        xlabel = xn_dict['xlabel']
        ylabel = xn_dict['y']['ylabel']
        xlist = xn_dict['xlist']
        ylist = xn_dict['y']['ylist']
        #开始画图
        fig = plt.figure(0 , figsize=(9*1.2 , 6*1.2))
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        for y in ylist:
            plt.plot(xlist , y['y_array'] , line_kinds() , label = y['label'])

        plt.legend(legend, loc=0, ncol=1)
        plt.xticks(xlist, xlist, size='small', rotation=30)
        plt.grid()
        plt.savefig('data_model/static/data_model/img/%s_plot.png'%title)
        #plt.show()
        plt.axis('off')
        plt.close()
    except Exception as e:
        print(e)
        #logger.error(e)
    return 'data_model/img/%s_plot.png'%title

def draw_bar(xn_dict,calllist):
    '''
    绘制柱状图
    :param xn_dict:
    :return:
    '''
    try:
        legend = [k['label'] for k in xn_dict['y']['ylist']]
        group_labels = xn_dict['group_labels']
        title = xn_dict['title']
        xlabel = xn_dict['xlabel']
        ylabel = xn_dict['y']['ylabel']
        xlist = xn_dict['xlist']
        ylist = xn_dict['y']['ylist']
        n = len(ylist)#每个横坐标分成n部分
        size = len(xlist)#找个作图的中间值便于计算偏移
        index=np.arange(1,size+1)
        total_width = 0.8
        width = total_width/n
        x = index-(total_width - width)/2

        fig = plt.figure(0, figsize=(9 * 1.2, 6 * 1.2))
        for i in range(n):#
            plt.bar( x+i*width, ylist[i]['y_array'] ,width=width)
        plt.legend(legend ,loc = 0 , ncol = 1 )
        plt.xticks( index+ width / 2, xlist, size='small', rotation=30)
        #plt.xticks(xlist, xlist, size='small', rotation=30)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        #plt.xticks(xlist, group_labels, rotation=0)
        plt.grid()
        plt.savefig('data_model/static/data_model/img/%s_bar.png' % title)
        #plt.show()
        plt.axis('off')
        plt.close()
    except Exception as e:
        print(e)
        #logger.error(e)
    return 'data_model/img/%s_bar.png' % title

def draw_scatter(xn_dict,calllist):
    '''
    绘制散点图
    :param xn_dict:
    :return:
    '''
    try:
        legend = [k['label'] for k in xn_dict['y']['ylist']]
        group_labels = xn_dict['group_labels']
        title = xn_dict['title']
        xlabel = xn_dict['xlabel']
        ylabel = xn_dict['y']['ylabel']
        xlist = xn_dict['xlist']
        ylist = xn_dict['y']['ylist']
        fig = plt.figure(0, figsize=(9 * 1.2, 6 * 1.2))
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        for y in ylist:
            plt.scatter(xlist , y['y_array'] , s=100,color= line_kinds()[0] , marker=line_kinds()[1] )
        plt.legend(legend, loc=0, ncol=1)
        plt.xticks(xlist, xlist, size='small', rotation=30)
        plt.savefig('data_model/static/data_model/img/%s_scatter.png' % title)
        #plt.show()
        plt.axis('off')
        plt.close()
    except Exception as e:
        print(e)
        #logger.error(e)
    return 'data_model/img/%s_scatter.png' % title

def draw_pie(xn_dict , calllist):
    '''
    绘制饼图
    :param xn_dict:
    :return:
    '''
    try:
        title = xn_dict['title']
        xlabel = xn_dict['xlabel']
        ylabel = xn_dict['y']['ylabel']
        xlist = xn_dict['xlist']
        group_labels = [y['label']for y in xn_dict['y']['ylist'] ]
        ylist = [y['y_array'] for y in xn_dict['y']['ylist']]
        #print('ylist' , ylist)
        fig=plt.figure(0, figsize=(9 * 1.2, 6 * 1.2))
        explode = []  # 各部分的突出zhi

        if len(ylist) == 1:
            for y in ylist[0]:
                explode.append(0.1)
            calllist_len = len(calllist)#总数
            ylist_pie = copy.deepcopy(ylist[0])
            ylist_pie.append(calllist_len)
            label_list_pie = copy.deepcopy(xlist)
            label_list_pie.append('all')
            explode.append(0)
        else:
            for y in ylist:
                explode.append(0.1)
            label_list_pie = copy.deepcopy(group_labels)
            ylist_pie = [sum(l) for l in ylist]
        explode= tuple(explode)
        colors = cm.rainbow(np.arange(len(label_list_pie))/len(label_list_pie))
        patches, texts, autotexts=plt.pie( ylist_pie , explode=explode , colors=colors ,radius=0.4,  labels=label_list_pie , labeldistance=1.1, autopct="%1.1f%%", shadow=False, startangle=90, pctdistance=0.9)
        plt.axis("equal")
        plt.title(title)
        # 重新设置字体大小
        proptease = fm.FontProperties()
        proptease.set_size('large')
        plt.setp(autotexts, fontproperties=proptease)
        plt.setp(texts, fontproperties=proptease)
        plt.legend(label_list_pie, loc=2)
        plt.savefig('data_model/static/data_model/img/%s_pie.png'%title)
        #plt.show()
        plt.axis('off')
        plt.close()
    except Exception as e:
        print(e)
        #logger.error(e)
    return 'data_model/img/%s_pie.png'%title

pic_dict={'plot':draw_plot,'bar':draw_bar,'pie':draw_pie,'scatter':draw_scatter}

def draw_pic(pic_categorylist , calllist , sample_range_xn_dict):
    '''
    绘制主函数
    :param pic_categorylist: 制图类型列表
    :param calllist: 通话记录
    :param sample_range_xn_dict_list: 样本范围为key的字典
    :return: 路由列表
    '''
    try:
        img_path = 'data_model/static/data_model/img'
        img_list =  os.listdir(img_path)
        if img_list:
            for img in img_list:
                os.remove(os.path.join(img_path , img))
    except Exception as e:
        print(e)
        #logger.error(e)
    result_list = []

    for pic in pic_categorylist:
        for xn_dict in sample_range_xn_dict:
            result_list.append(pic_dict[pic](sample_range_xn_dict[xn_dict] , calllist))

    return result_list

if __name__=='__main__':
    calllist = [1,2,3,4,5,6,6,7,8,8,3,6,6,5,4,34,3,3,3]
    x= {
        'title': 'xxxx',
        'xlabel': 'xlabel',
        'xlist': [1,2,3,4],
        'group_labels': ['one' , 'two' , 'three' ],
        'y': {
            'ylabel': 'y_lab',
            'ylist': [
                {
                    'label': '早晨',
                    'y_array': [1,2,3]
                },
                {
                    'label': 'noon',
                    'y_array': [1, 4, 5, 3]
                }
                      ]
            }
    }
    draw_plot(x , calllist)
    #draw_bar(x , calllist)
    #draw_scatter(x , calllist)
    #draw_pie(x, calllist)

