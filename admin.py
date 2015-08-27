from __future__ import unicode_literals
from .models import WorkOrderPage, EmployeesPage, WorkOrder, Employee
from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from mezzanine.core.admin import TabularDynamicInlineAdmin, SingletonAdmin

admin.site.register(WorkOrderPage, PageAdmin)
admin.site.register(EmployeesPage, PageAdmin)
admin.site.register(WorkOrder)


class WorkOrderInline(TabularDynamicInlineAdmin):
    model = WorkOrder
	
# 
class WorkOrderAdmin(admin.ModelAdmin):
    inlines = [WorkOrderInline,]
	#fieldsets = ((None, {"fields": ("title",)}),)



admin.site.register(Employee,WorkOrderAdmin )
#admin.site.register(Employee)



from django.contrib import admin
from mezzanine.core.admin import TabularDynamicInlineAdmin, SingletonAdmin

from copy import deepcopy
from .models import Work, WorkImage


class WorkImageInline(TabularDynamicInlineAdmin):
    model = WorkImage
	
 
class WorkAdmin(admin.ModelAdmin):
    inlines = [WorkImageInline,]
	#fieldsets = ((None, {"fields": ("title",)}),)



admin.site.register(Work, WorkAdmin)