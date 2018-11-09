from django.shortcuts import render , redirect
from django.http import HttpResponse
import json , os
from util.parsedata import Parse
from util.filter import calculation_filter , pic_filter
from util.matplotpaint import draw_pic
from util import calculate
import logging
import time
import hashlib
import copy
from .models import File_table,Otherarea_table,Call_table
#logger = logging.getLogger('sourceDns.webdns.views')

f_data = ''
result_f_name_dict = {}
def index(request):
    if request.is_ajax():
        message = {'msg':'正在上传请稍后......'}
        return HttpResponse(json.dumps(message))
    return render(request , "data_model/index.html" )

def upload(request):
    '''
    显示上传页面
    :param request:
    :return:
    '''

    if request.method == "POST":
        f_name_dict = {}  # 用以存储文件名->时间的键值对，便于查询
        f_name_list = []  # 用以存储文件名返回给前端模板
        otherarealist = []
        files = request.FILES.getlist('myfile')
        f = File_table()
        if files:
            for file in files:
                hash = hashlib.sha256()
                t = str(time.time())
                hash.update(str(time.time()).encode('utf8') )
                f_time = hash.hexdigest()    #上传时间
                f_name = file.name           #文件名
                time.sleep(0.000001)
                if file:
                    file_path = os.path.join('myfile',f_name)
                    with open(file_path, 'wb') as fp:
                        try:
                            for chunk in file.chunks():
                                fp.write(chunk)
                        except UnicodeError as e:
                            print(e)
                            #logger.error(e)
                    with open(file_path, 'rb') as fp:
                        global f_data
                        f_data = fp.read()
                        try:
                            f_data = json.loads(f_data)
                        except Exception as e:
                            print(e)
                            #logger.error(e)
                        otherarealist_s , otherarea_table= Parse.parse_otherarea_list(f_data , f_time)    #归属地
                        # 还差通话记录
                        call_table = Parse.parse_newcalllist_sql(f_data ,f_time )
                        f_name_list.append(f_name)
                        f_name_dict[f_name] = f_time
                        f = File_table(f_time = f_time , f_name = f_name ,otherarea_table = otherarea_table , call_table = call_table )
                        f.save()
            global result_f_name_dict
            result_f_name_dict= copy.deepcopy(f_name_dict)

        if request.is_ajax():
            '''需要对otherarealist逻辑进行更改'''
            pk = request.POST.get('f_time')
            #print('pk',pk)
            otherareatable = Otherarea_table.objects.filter(f_time=pk)
            otherarealist = [o.name for o in otherareatable]
            result_dict = {}
            if otherarealist:
                result_dict['otherarelist']=otherarealist
            else:
                result_dict['otherarelist'] =['无归属地',]
            result_dict_str = json.dumps(result_dict)
            #设置cookie
            response = HttpResponse(result_dict_str)
            response.set_cookie('f_name_dict', json.dumps(result_f_name_dict), expires=60 * 60 * 24 * 7)
            return response

    return render(request, "data_model/upload.html", context={ 'filenames': f_name_dict})

def output(request):
    '''
    处理选中的数据
    :param request:
    :return:
    '''
    if request.method == "POST":
        try:
            daytimelist = request.POST.getlist('daytime')#通话时段
            calltypelist = request.POST.getlist('calltype')#通话类型
            landtypelist = request.POST.getlist('landtype')#通话所在地
            phonetypelist = request.POST.getlist('phonetype')#号码类型
            phonepropertylist = request.POST.getlist('phoneproperty')#号码性质
            otherarealist = request.POST.getlist('otherarealist')#对方号码归属地
            sample_rangelist= request.POST.getlist('sample_range')#样本范围
            pic_categorylist = request.POST.getlist('pic_category')#制图分类
            calculationlist = request.POST.getlist('calculation')#计算方式
        except Exception as e:
            print(e)
            #logger.error(e)
        global f_data
        calllist = Parse.parse_oldcalllist(f_data)  # 通话记录
        newcalllist = Parse.parse_newcalllist(f_data)  # 新的联系人列表
        #计算方式处理开始
        last_cal_step_list = calculation_filter(newcalllist,daytimelist,calltypelist,landtypelist ,phonetypelist ,phonepropertylist ,otherarealist)#计算方式过滤器
        calculate_result = calculate.calculate(calllist, sample_rangelist, last_cal_step_list, calculationlist)
        count_call_dict = {}
        if 'count_call'  in calculationlist:
            count_call_dict = calculate_result['count_call']
        sum_calllong_dict={}
        if 'sum_calllong' in calculationlist:
            sum_calllong_dict = calculate_result['sum_calllong']
        ratio_dict={}
        if 'ratio' in calculationlist:
            ratio_dict=calculate_result['ratio']
        count_group_by_otherarea_dict={}
        if 'count_group_by_otherarea' in calculationlist:
            count_group_by_otherarea_dict = calculate_result['count_group_by_otherarea']
        #print("count_call_dict",count_call_dict)
        #计算方式处理结束

        # 绘图策略处理
        last_pic_step_list, legend_list = pic_filter(newcalllist, daytimelist, calltypelist, landtypelist,phonetypelist, phonepropertylist, otherarealist)
        sample_range_xn_dict_list = calculate.pic_calculate(last_pic_step_list, legend_list, sample_rangelist,calllist , otherarealist )
        images_list = []
        try:
            images_list = draw_pic(pic_categorylist, calllist, sample_range_xn_dict_list)
        except RuntimeError as e:
            print(e)
            #logger.error(e)
        f_name_dict = json.loads(request.COOKIES.get('f_name_dict'))
        #print('f_name_dict---------',type(f_name_dict))
        return render(request , "data_model/output.html" ,
                  context={'images': images_list,
                           'count_call_dict' : count_call_dict ,
                           'sum_calllong_dict':sum_calllong_dict,
                           'ratio_dict':ratio_dict,
                           'count_group_by_otherarea_dict':count_group_by_otherarea_dict,
                           'filenames' : f_name_dict,
                           } )


