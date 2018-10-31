#!/usr/bin/env python
#-*-coding:utf-8-*-
import datetime , copy
import pandas as pd
import logging
logger = logging.getLogger('scripts')
class Samplerange:
    samplerange_dict={
        'all' : 6,
        'one_month':1,
        'three_months':3,
        'six_months':6
    }
    @classmethod
    def get_sample_range(cls , sample_rangelist , calllist):
        '''
        计算样本范围的开始结束时间，并根据样本范围列表返回一个带起止时间的字典
        :param sample_rangelist: 样本范围的列表
        :param calllist: 所有的通话记录列表，求起止时间会用到
        :return:
        '''
        sample_range_dict = {}
        try:
            for sample in sample_rangelist:
                start_end_dict ={}
                start , end = cls.get_start_and_end_time(calllist ,cls.samplerange_dict[sample])
                start_end_dict['start'] = start
                start_end_dict['end'] = end
                sample_range_dict[sample] = copy.deepcopy(start_end_dict)
        except Exception as e:
            logger.error(e)
        #print(sample_range_dict)
        return sample_range_dict

    @classmethod
    def get_timestamp(cls,date):
        '''
        排序规则函数,将时间转换成秒数并返回
        :param date: str类型的时间
        :return: 从格林尼治时间开始计算得道秒数
        '''
        return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').timestamp()

    @classmethod
    def get_strptime(cls,date):
        '''
        转换成datetime类型
        :param date:str类型时间
        :return: 返回datetime类型
        '''
        return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    @classmethod
    def get_time_nm_ago(cls ,calllist, n):
        '''
        获取最近n个月以前的时间
        :param calllist:
        :return:
        '''
        try:
            time_1m_ago = ''
            timeList = []
            for call in calllist:
                timeList.append(call['calltime'])
            tempTimeList = sorted(timeList, key=lambda date: cls.get_timestamp(date))
            time_now = cls.get_strptime(tempTimeList[len(tempTimeList) - 1])
            time_now_year = time_now.year
            time_now_month = time_now.month + 1
            time_now_day = time_now.day
            time_now_hour = time_now.hour
            time_now_min = time_now.minute
            time_now_sec = time_now.second
            if time_now_month > 12:
                time_now_month = 1
                time_now_year = time_now_year + 1
            temp_time_now = datetime.datetime(time_now_year, time_now_month, time_now_day, time_now_hour, time_now_min,
                                              time_now_sec)
            pd_time_now = temp_time_now.strftime('%Y%m%d%H%M%S')
            pd_list = pd.date_range('201501010000', pd_time_now, freq='1M')
            days = (pd_list[-1] - pd_list[-n - 1]).days
            time_1m_ago = datetime.datetime.strftime(time_now - datetime.timedelta(days=days), '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            logger.error(e)
        return time_1m_ago

    @classmethod
    def get_start_and_end_time(cls,someList, n):
        '''
        计算几个月之前的起止时间
        :param someList:
        :param n:
        :return:
        '''
        try:
            now = cls.get_time_nm_ago(someList, 0)
            day = cls.get_strptime(now).day
            endtime = datetime.datetime(2015, 1, 1)
            starttime = datetime.datetime(2015, 1, 1)
            temp = 0
            if day <= 15:
                temp = n
                endtime = datetime.datetime(cls.get_strptime(now).year, cls.get_strptime(now).month, day) - datetime.timedelta(
                    days=day)
            else:
                temp = n - 1
                endtime = cls.get_strptime(now)
            if temp != 0:
                pre = datetime.datetime(cls.get_strptime(now).year, cls.get_strptime(now).month, 1).strftime('%Y%m%d')
                # print('pre',pre)
                monlist = pd.date_range('20150101', pre, freq='1M')
                # print(monlist)
                starttime = str(monlist[-temp])
                startdays = datetime.datetime.strptime(starttime, '%Y-%m-%d %H:%M:%S').day
                starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(
                    days=startdays - 1)
            else:
                starttime_1 = cls.get_strptime(now) - datetime.timedelta(days=cls.get_strptime(now).day - 1)
                starttime_1_year = starttime_1.year
                starttime_1_month = starttime_1.month
                starttime_1_day = starttime_1.day
                starttime = datetime.datetime(starttime_1_year, starttime_1_month, starttime_1_day, 0, 0, 0)
            starttime = datetime.datetime.strftime(starttime, '%Y-%m-%d %H:%M:%S')
            endtime = datetime.datetime.strftime(endtime, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            logger.error(e)
        return starttime, endtime

#无时分秒
class Samplerange_simple:
    samplerange_dict={
        'all' : 8,
        'one_month':1,
        'three_months':4,
        'six_months':7
    }
    @classmethod
    def get_sample_range(cls , sample_rangelist , calllist):
        '''
        计算样本范围的开始结束时间，并根据样本范围列表返回一个带起止时间的字典
        :param sample_rangelist: 样本范围的列表
        :param calllist: 所有的通话记录列表，求起止时间会用到
        :return:
        '''
        sample_range_dict = {}
        try:
            for sample in sample_rangelist:
                start_end_dict ={}
                start , end = cls.get_start_and_end_time(calllist ,cls.samplerange_dict[sample])
                start_end_dict['start'] = start
                start_end_dict['end'] = end
                sample_range_dict[sample] = copy.deepcopy(start_end_dict)
            #print(sample_range_dict)
        except Exception as e:
            logger.error(e)
        return sample_range_dict

    @classmethod
    def get_timestamp(cls,date):
        '''
        排序规则函数,将时间转换成秒数并返回
        :param date: str类型的时间
        :return: 从格林尼治时间开始计算得道秒数
        '''
        return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').timestamp()

    @classmethod
    def get_strptime(cls,date):
        '''
        转换成datetime类型
        :param date:str类型时间
        :return: 返回datetime类型
        '''
        return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    @classmethod
    def get_time_nm_ago(cls ,calllist, n):
        '''
        获取最近n个月以前的时间
        :param calllist:
        :return:
        '''
        time_1m_ago = ''
        timeList = []
        for call in calllist:
            timeList.append(call['calltime'])
        tempTimeList = sorted(timeList, key=lambda date: cls.get_timestamp(date))
        time_now = cls.get_strptime(tempTimeList[len(tempTimeList) - 1])
        time_now_year = time_now.year
        time_now_month = time_now.month + 1
        time_now_day = time_now.day
        time_now_hour = time_now.hour
        time_now_min = time_now.minute
        time_now_sec = time_now.second
        if time_now_month > 12:
            time_now_month = 1
            time_now_year = time_now_year + 1
        temp_time_now = datetime.datetime(time_now_year, time_now_month, time_now_day, time_now_hour, time_now_min,
                                          time_now_sec)
        pd_time_now = temp_time_now.strftime('%Y%m%d%H%M%S')
        pd_list = pd.date_range('201501010000', pd_time_now, freq='1M')
        days = (pd_list[-1] - pd_list[-n - 1]).days
        time_1m_ago = datetime.datetime.strftime(time_now - datetime.timedelta(days=days), '%Y-%m-%d %H:%M:%S')
        return time_1m_ago

    @classmethod
    def get_start_and_end_time(cls,someList, n):
        '''
        计算几个月之前的起止时间
        :param someList:
        :param n:
        :return:
        '''
        now = cls.get_time_nm_ago(someList, 0)
        # print('now',now)
        day = cls.get_strptime(now).day

        endtime = datetime.datetime(2015, 1, 1)
        starttime = datetime.datetime(2015, 1, 1)
        temp = 0
        if day <= 15:
            temp = n
            endtime = datetime.datetime(cls.get_strptime(now).year, cls.get_strptime(now).month, day) - datetime.timedelta(
                days=day)
        else:
            temp = n - 1
            endtime = cls.get_strptime(now)
        if temp != 0:
            pre = datetime.datetime(cls.get_strptime(now).year, cls.get_strptime(now).month, 1).strftime('%Y%m%d')
            # print('pre',pre)
            monlist = pd.date_range('20150101', pre, freq='1M')
            # print(monlist)
            starttime = str(monlist[-temp])
            startdays = datetime.datetime.strptime(starttime, '%Y-%m-%d %H:%M:%S').day
            starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(
                days=startdays - 1)
        else:
            starttime_1 = cls.get_strptime(now) - datetime.timedelta(days=cls.get_strptime(now).day - 1)
            starttime_1_year = starttime_1.year
            starttime_1_month = starttime_1.month
            starttime_1_day = starttime_1.day
            starttime = datetime.datetime(starttime_1_year, starttime_1_month, starttime_1_day, 0, 0, 0)
        starttime = datetime.datetime.strftime(starttime, '%Y-%m-%d')
        endtime = datetime.datetime.strftime(endtime, '%Y-%m-%d')
        return starttime, endtime

if __name__=='__main__':
    import json
    with open('元数据/陈虎_17721396513.txt','rb') as fp:
        file_data = json.loads(fp.read())
        calllist = file_data['operatorReport']['callVOList']
        print(calllist)
        Samplerange.get_start_and_end_time(calllist , 10)
        sample_range_list = ['all' , 'one_month' , 'three_months' , 'six_months']
        Samplerange.get_sample_range(sample_range_list , calllist)