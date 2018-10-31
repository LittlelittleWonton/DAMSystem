from django.shortcuts import render , redirect
from django.http import HttpResponse
import json , os
from util.parsedata import Parse
from util.filter import calculation_filter , pic_filter
from util.matplotpaint import draw_pic
from util import calculate
import logging
logger = logging.getLogger('sourceDns.webdns.views')

f_data = ''
otherarealist = []
def index(request):
    homelist=[]
    if request.method == "POST":
        
        obj = request.FILES.get('myfile')
        if obj:
            file_path = os.path.join('myfile',obj.name)
            with open(file_path, 'wb') as fp:
                try:
                    for chunk in obj.chunks():
                        fp.write(chunk)
                except UnicodeError as e:
                    logger.error(e)
            with open(file_path, 'rb') as fp:
                global f_data
                f_data = fp.read()
                #print(type(f_data))
                try:
                    f_data = json.loads(f_data)
                except Exception as e:
                    logger.error(e)
                global otherarealist
                otherarealist = Parse.parse_otherarea_list(f_data)
        else:
            otherarealist = []

    return render(request , "data_model/index.html" , context={ 'homelist' : otherarealist})

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
            logger.error(e)
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
            #print(";);););););)images_list" , images_list)
        except RuntimeError as e:
            logger.error(e)
        return render(request , "data_model/output.html" ,
                  context={'images': images_list,
                           'count_call_dict' : count_call_dict ,
                           'sum_calllong_dict':sum_calllong_dict,
                           'ratio_dict':ratio_dict,
                           'count_group_by_otherarea_dict':count_group_by_otherarea_dict,

                           } )


