from django.contrib import admin

# Register your models here.
from .models import Call_table, Otherarea_table, File_table

# class NiuXinAdminSite(admin.AdminSite):
    # site_header = 'DMAS Admin'  # 此处设置页面显示标题
    # site_title = 'Data Model Analysis System Admin'  # 此处设置页面头部标题
# admin_site = NiuXinAdminSite(name='management')

class Call_table_Admin(admin.ModelAdmin):
    list_display = ['f_time', 'callday', 'calltime', 'calllong', 'daytime', 'calltype', 'landtype','phonetype', 'callphone', 'otherarea', 'homearea', 'month', 'phoneproperty']
    search_fields =['f_time', 'callday', 'calltime', 'calllong', 'daytime', 'calltype', 'landtype','phonetype', 'callphone', 'month', 'phoneproperty'] #搜索字段
   	
class Otherarea_table_Admin(admin.ModelAdmin):
    list_display = ['f_time', 'name']
    search_fields = ['f_time', 'name']

class File_table_Admin(admin.ModelAdmin):
    list_display = ['f_time', 'f_name', 'otherarea_table', 'call_table']
    search_fields = ['f_time', 'f_name', 'otherarea_table', 'call_table']
 

admin.site.register(Call_table,Call_table_Admin)
admin.site.register(Otherarea_table,Otherarea_table_Admin)
admin.site.register(File_table, File_table_Admin)
admin.site.site_header = 'DMAS Admin'
admin.site.site_title = 'Data Model Analysis System Admin'