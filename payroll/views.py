from django.shortcuts import render
from .models import Employee, Payroll
from .forms import EmployeeForm, UserForm,PayrollForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def dashboard(request):
    total_employees = Employee.objects.count()
    total_payrolls = Payroll.objects.count()  # Changed from Payslip to Payroll
    return render(request, 'payroll/dashboard.html', {
        'total_employees': total_employees,
        'total_payrolls': total_payrolls  # Changed variable name
    })
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'payroll/employee_list.html', {'employees': employees})

def payslip_list(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    payrolls = Payroll.objects.filter(employee=employee).order_by('-month')
    
    # Debugging output
    print(f"Employee: {employee}")
    print(f"Found {payrolls.count()} payroll records")
    for p in payrolls:
        print(f"Payroll: {p.month} - {p.net_salary}")
    
    return render(request, 'payroll/payslip_list.html', {
        'employee': employee,
        'payslips': payrolls
    })

def add_employee(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        employee_form = EmployeeForm(request.POST)

        if user_form.is_valid() and employee_form.is_valid():
            user = user_form.save()
            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()
            return redirect('employee_list')
    else:
        user_form = UserForm()
        employee_form = EmployeeForm()

    return render(request, 'payroll/add_employee.html', {
        'user_form': user_form,
        'employee_form': employee_form,
    })
def generate_payroll(request):
    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            payroll = form.save(commit=False)
            # net_salary is automatically calculated in the model's save()
            payroll.save()
            return redirect('dashboard')
    else:
        form = PayrollForm()
    return render(request, 'payroll/generate_payroll.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'payroll/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')