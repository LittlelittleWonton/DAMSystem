#!/usr/bin/env python
#-*-coding:utf-8-*-
import logging
#logger = logging.getLogger('scripts')
def calculation_filter(newcalllist,daytimelist,calltypelist,landtypelist ,phonetypelist ,phonepropertylist ,otherarealist):
    '''
    计算方式过滤器
    :param newcalllist:
    :param daytimelist:
    :param calltypelist:
    :param landtypelist:
    :param phonetypelist:
    :param phonepropertylist:
    :param otherarealist:
    :return:
    '''
    try:
        # 第一遍过滤
        step_1_list = []
        if 'all' in daytimelist or len(daytimelist) == 0:
            step_1_list = newcalllist
        else:
            for call in newcalllist:
                if call['daytime'] in daytimelist:
                    step_1_list.append(call)
        # print('step_1_list', len(step_1_list))
        # 第二遍过滤
        step_2_list = []
        if 'all' in calltypelist or len(calltypelist) == 0:
            step_2_list = step_1_list
        else:
            for call in step_1_list:
                if call['calltype'] in calltypelist:
                    step_2_list.append(call)
        # print('step_2_list', len(step_2_list))
        # 第三遍过滤
        step_3_list = []
        if 'all' in landtypelist or len(landtypelist) == 0:
            step_3_list = step_2_list
        else:
            for call in step_2_list:
                if call['landtype'] in landtypelist:
                    step_3_list.append(call)
        # print('step_3_list', len(step_3_list))
        # 第四遍过滤
        step_4_list = []
        if 'all' in phonetypelist or len(phonetypelist) == 0:
            step_4_list = step_3_list
        else:
            for call in step_3_list:
                if call['phonetype'] in phonetypelist:
                    step_4_list.append(call)
        # print('step_4_list', len(step_4_list))
        # 第五遍过滤
        step_5_list = []
        if 'all' in phonepropertylist or len(phonepropertylist) == 0:
            step_5_list = step_4_list
        else:
            for call in step_4_list:
                if call['phoneproperty'] in phonepropertylist:
                    step_5_list.append(call)
        # print('step_5_list', len(step_5_list))
        # 第六遍过滤
        step_6_list = []
        if 'all' in otherarealist or len(otherarealist) == 0:
            step_6_list = step_5_list
        else:
            for call in step_5_list:
                if call['otherarea'] in otherarealist:
                    step_6_list.append(call)
        # print('step_6_list',len(step_6_list))
        # print('step_6_list', step_6_list)
    except Exception as e:
        logging.error(e)
    return  step_6_list

class AllList(object):

    def __init__(self, flag , real_list):
        self.flag = flag
        self.real_list = real_list

def pic_filter(newcalllist,daytimelist,calltypelist,landtypelist ,phonetypelist ,phonepropertylist ,otherarealist):
    '''
    图片过滤器
    :param newcalllist:
    :param daytimelist:
    :param calltypelist:
    :param landtypelist:
    :param phonetypelist:
    :param phonepropertylist:
    :param otherarealist:
    :return:
    '''
    try:
        daytimelist = AllList(0 , daytimelist)
        calltypelist = AllList(0, calltypelist)
        landtypelist = AllList(0, landtypelist)
        phonetypelist = AllList(0, phonetypelist)
        phonepropertylist = AllList(0, phonepropertylist)
        otherarealist = AllList(0, otherarealist)
        #judge
        judge_list = []
        # 第一遍过滤
        step_1_list = []
        if 'all' in daytimelist.real_list or len(daytimelist.real_list) == 0:
            step_1_list = newcalllist
        else:
            daytimelist.flag=1
            judge_list.append(daytimelist)
            for call in newcalllist:
                if call['daytime'] in daytimelist.real_list:
                    step_1_list.append(call)
        # print('step_1_list', len(step_1_list))
        # 第二遍过滤
        step_2_list = []
        if 'all' in calltypelist.real_list or len(calltypelist.real_list) == 0:
            step_2_list = step_1_list
        else:
            calltypelist.flag = 1
            judge_list.append(calltypelist)
            for call in step_1_list:
                if call['calltype'] in calltypelist.real_list:
                    step_2_list.append(call)
        # print('step_2_list', len(step_2_list))
        # 第三遍过滤
        step_3_list = []
        if 'all' in landtypelist.real_list or len(landtypelist.real_list) == 0:
            step_3_list = step_2_list
        else:
            landtypelist.flag=1
            judge_list.append(landtypelist)
            for call in step_2_list:
                if call['landtype'] in landtypelist.real_list:
                    step_3_list.append(call)
        # print('step_3_list', len(step_3_list))
        # 第四遍过滤
        step_4_list = []
        if 'all' in phonetypelist.real_list or len(phonetypelist.real_list) == 0:
            step_4_list = step_3_list
        else:
            phonetypelist.flag=1
            judge_list.append(phonetypelist)
            for call in step_3_list:
                if call['phonetype'] in phonetypelist.real_list:
                    step_4_list.append(call)
        # print('step_4_list', len(step_4_list))
        # 第五遍过滤
        step_5_list = []
        if 'all' in phonepropertylist.real_list or len(phonepropertylist.real_list) == 0:
            step_5_list = step_4_list
        else:
            phonepropertylist.flag=1
            judge_list.append(phonepropertylist)
            for call in step_4_list:
                if call['phoneproperty'] in phonepropertylist.real_list:
                    step_5_list.append(call)
        # print('step_5_list', len(step_5_list))
        # 第六遍过滤
        step_6_list = []
        if 'all' in otherarealist.real_list or len(otherarealist.real_list) == 0:
            step_6_list = step_5_list
        else:
            otherarealist.flag=1
            judge_list.append(otherarealist)
            for call in step_5_list:
                if call['otherarea'] in otherarealist.real_list:
                    step_6_list.append(call)
        # print('step_6_list',len(step_6_list))
        # print('step_6_list', step_6_list)
        for call in step_6_list:
            call['calltime'] = call['calltime'][:10]

        sum = 0
        for ele in judge_list:
            sum+=ele.flag
    except Exception as e:
        print(e)
        #logger.error(e)

    if sum ==0 or sum>1:
        return step_6_list , []
    elif sum ==1:
        for ele in judge_list:
            if ele.flag==1:
                return step_6_list , ele.real_list
