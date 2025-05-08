from django.contrib import admin
from .models import Department, Employee, Attendance, Payroll

# Register your models here
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(Payroll)
