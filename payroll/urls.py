from django.urls import path
from . import views
from .views import dashboard, add_employee, generate_payroll, user_login, user_logout

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('employees/', views.employee_list, name='employee_list'),
    path('payslips/<int:employee_id>/', views.payslip_list, name='payslip_list'),
    path('', dashboard, name='dashboard'),
    path('add-employee/', add_employee, name='add_employee'),
    path('generate-payroll/', generate_payroll, name='generate_payroll'),
]