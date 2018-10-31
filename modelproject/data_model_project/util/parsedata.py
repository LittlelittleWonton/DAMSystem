#!/usr/bin/env python
#-*-coding:utf-8-*-
import json
import datetime
import re
import copy
import requests
import logging

logger = logging.getLogger('scripts')
class Parse(object):

    @classmethod
    def parse_otherarea_list(cls,person_data):
        '''
        归属地
        :param path:
        :return:
        '''
        otherarealist = []
        try:
            calllist = person_data['operatorReport']['callVOList']
            if len(calllist) == 0:
                return []
            templist = [call['otherarea'] for call in calllist if 'otherarea' in call ]
            otherarealist = list(set(templist))
        except Exception as e:
          logger.error(e)
        #print(otherarealist)
        return otherarealist

    @classmethod
    def parse_newcalllist(cls , f_data):
        '''
        获取改装之后的calllist
        :param path:
        :return:
        '''
        '''
        calltimelist = request.POST.getlist('calltime')#通话时段
        calltypelist = request.POST.getlist('calltype')#通话类型
        homearealist = request.POST.getlist('homearea')#通话所在地
        phonetypelist = request.POST.getlist('phonetype')#号码类型
        phonepropertylist = request.POST.getlist('phoneproperty')#号码性质
        otherarealist = request.POST.getlist('otherarealist')#对方号码归属地
        sample_rangelist= request.POST.getlist('sample_range')#样本范围
        pic_categorylist = request.POST.getlist('pic_category')#制图分类
        calculationlist = request.POST.getlist('calculation')#计算方式
        '''
        comcalllist = []
        try:

            calllist = f_data['operatorReport']['callVOList']
            phone_property = cls._get_phoneproperty(calllist)
            if len(calllist) ==0:
                return []
            for call in calllist:
                newcall = {}
                #calltime datatime
                if 'calltime' in call:
                    if call['calltime']:
                        newcall['daytime'] = cls._judge_stat(cls._get_strptime(call['calltime']))
                        newcall['calltime'] = call['calltime']
                        newcall['callday'] = call['calltime'][:10]
                    else:
                        newcall['daytime'] = 'E-5'
                        newcall['calltime'] = '2000-01-01 00:00:00'
                else:
                    newcall['daytime'] = 'E-5'
                    newcall['calltime'] = '2000-01-01 00:00:00'
                #calllong
                if 'calllong' in call:
                    if call['calllong']:
                        newcall['calllong'] = int(call['calllong'])
                    else:
                        newcall['calllong'] = 0
                else:
                    newcall['calllong'] = 0
                if 'calltype' in call:
                    if call['calltype']:
                        if call['calltype'] == '被叫':
                            newcall['calltype'] = 'called'
                        elif call['calltype'] == '主叫':
                            newcall['calltype'] = 'calling'
                    else:
                        newcall['calltype'] = 'E-5'
                else:
                    newcall['calltype'] = 'E-5'
                #landtype
                if 'landtype' in call:
                    if call['landtype']:
                        pat = re.compile('^.*本.*地.*$')
                        a = pat.match(call['landtype'])
                        if a :
                            newcall['landtype'] = "local"
                        else:
                            newcall['landtype'] = "allopatry"
                    else:
                        newcall['landtype'] = 'E-5'
                else:
                    newcall['landtype'] = 'E-5'
                #callphone phonetype
                if 'callphone' in call:

                    if call['callphone']:
                        newcall['callphone'] = call['callphone']

                        pat = re.compile(r'^((1[0-9][0-9]))\d{8}$')
                        a = pat.match(call['callphone'])
                        if a:
                            newcall['phonetype'] = 'mobile'
                        else:
                            newcall['phonetype'] = 'tel'
                    else:
                        newcall['callphone'] = 'E-5'
                        newcall['phonetype'] = 'E-5'
                else:
                    newcall['callphone'] = 'E-5'
                    newcall['phonetype'] = 'E-5'
                #otherarea
                if 'otherarea' in call:
                    if call['otherarea']:
                        newcall['otherarea'] = call['otherarea']
                    else:
                        newcall['otherarea'] = 'E-5'
                else:
                    newcall['otherarea'] = 'E-5'
                #homearea
                if 'homearea' in call:
                    if call['homearea'] :
                        newcall['homearea'] = call['homearea']
                    else:
                        newcall['homearea'] = 'E-5'
                else:
                    newcall['month'] = 'E-5'
                # homearea
                if 'month' in call:
                    if call['month']:
                        newcall['month'] = call['month']
                    else:
                        newcall['month'] = 'E-5'
                else:
                    newcall['month'] = 'E-5'
                #phoneproperty
                newcall['phoneproperty'] = phone_property[call['callphone']]
                comcalllist.append(copy.deepcopy(newcall))
        except Exception as e:
            logger.error(e)
        #print(comcalllist)
        return comcalllist

    @classmethod
    def parse_oldcalllist(cls,f_data):
        return f_data['operatorReport']['callVOList']

    def _get_timestamp(date):
            '''
            排序规则函数
            :param date: str类型的时间
            :return: 从格林尼治时间开始计算得道秒数
            '''
            return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').timestamp()

    def _get_strptime(date):
            '''
            转换成日期类型
            :param date:str类型时间
            :return: 返回日期类型
            '''
            return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    def _judge_stat(time_stat):
            stat = ''
            h = time_stat.hour
            if h >= 2 and h < 6:
                stat = 'early_morning'
            elif h >= 6 and h < 10:
                stat = 'morning'
            elif h >= 10 and h < 14:
                stat = 'noon'
            elif h >= 14 and h < 18:
                stat = 'afternoon'
            elif h >= 18 and h < 22:
                stat = 'early_night'
            elif 24 > h >= 22 or 0 <= h < 2:
                stat = 'night'
            return stat
    @classmethod
    def _get_phoneproperty(cls , calllist):

        '''
        获取一个电话属性的字典形列表
        :param calllist: 通话记录
        :return: 返回字典类型的列表
        '''

        result_dict = {}
        try:
            phonenum_list = list(set([call['callphone'] for call in calllist]))
            url = r"http://risk.51nbapi.com/risktext//phone/financial/label/queryList?phones="
            x = 0
            while x < len(phonenum_list):
                phones = []
                if x+100 <len(phonenum_list):
                    phones = phonenum_list[x:x+100]
                else:
                    phones = phonenum_list[x:-1]
                x = x + 100
                #print(phones)
                nums = json.dumps(phones)
                url_nums = ''.join((url , nums))
                try:
                    result = requests.get(url_nums)
                except  TimeoutError as e :
                    logger.error(e)
                temp_dict = json.loads(json.loads(result.text)['data'])

                result_dict.update(temp_dict)
            for num in phonenum_list:
                if num not in result_dict:
                    result_dict[num] = '未知'
        except Exception as e:
            logger.error(e)
        return result_dict




if __name__ =='__main__':
    pass
    #other = Parse.parse_otherarea_list('元数据/陈鸿勇_18777542225.txt')

    #com = Parse.parse_calllist('元数据/陈虎_17721396513.txt')


