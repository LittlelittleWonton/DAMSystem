from django.db import models

class Call_table(models.Model):
    '''
    通话记录表
    '''
    f_time = models.CharField( max_length=80, null=False, blank=False, verbose_name="文件上传时间")
    callday = models.CharField(max_length = 30,null = False , blank = False, verbose_name = "通话时间(精确到天)")
    calltime = models.CharField(max_length = 30,null = False , blank = False, verbose_name = "通话时间(精确到秒)")
    calllong = models.IntegerField(null = False , blank = False, verbose_name = "通话时长(精确到秒)")
    daytime = models.CharField(max_length = 30,null = False , blank = False, verbose_name = "通话时段")
    calltype = models.CharField(max_length = 30,null = False , blank = False, verbose_name = "主被叫")
    landtype = models.CharField(max_length = 30,null = False , blank = False, verbose_name = "本地异地")
    phonetype = models.CharField(max_length = 30,null = False , blank = False, verbose_name = "座机手机")
    callphone = models.CharField(max_length = 30,null = False , blank = False, verbose_name = "电话号码")
    otherarea = models.CharField(max_length = 40,null = False , blank = False, verbose_name = "对方归属地")
    homearea = models.CharField(max_length = 40,null = False , blank = False, verbose_name = "本机归属地")
    month = models.CharField(max_length = 20,null = False , blank = False, verbose_name = "通话时间(精确到月)")
    phoneproperty = models.CharField(max_length = 20,null = False , blank = False, verbose_name = "号码性质")

    def __str__(self):
        return self.callphone

class Otherarea_table(models.Model):
    '''
    归属地表
    '''
    f_time = models.CharField( max_length=80, null=False, blank=False, verbose_name="文件上传时间")
    name = models.CharField(max_length = 30,null = False , blank = False, verbose_name = "归属地")

    def __str__(self):
        return self.name

class File_table(models.Model):
    '''
    文件表
    '''
    f_time = models.CharField(primary_key= True,max_length = 80,null = False , blank = False, verbose_name = "文件上传时间")
    f_name = models.CharField(max_length = 40,null = False , blank = False, verbose_name = "文件名")
    otherarea_table = models.ForeignKey(Otherarea_table , blank = True , null = False , on_delete=models.CASCADE)
    call_table = models.ForeignKey(Call_table, blank = True , null = False , on_delete=models.CASCADE )
