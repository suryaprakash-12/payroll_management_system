from django import forms
from django.contrib.auth.models import User
from .models import Employee, Payroll,Department

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class EmployeeForm(forms.ModelForm):
    department = forms.CharField(
        label="Department", 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter department name'})
    )

    class Meta:
        model = Employee
        fields = ['department', 'salary', 'join_date']

    def clean_department(self):
        department_name = self.cleaned_data['department']
        department, created = Department.objects.get_or_create(name=department_name)
        return department
    
class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = [
            'employee', 
            'month', 
            'basic_salary', 
            'tax_deduction', 
            'bonus', 
            'other_deductions'
        ]
        # net_salary is auto-calculated, so we don't include it in the form