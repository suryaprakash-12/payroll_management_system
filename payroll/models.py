from django.db import models
from django.contrib.auth.models import User

# Department Model
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Employee Model
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    join_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

# Attendance Model
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.employee.user.first_name} - {self.date} - {self.status}"

# Payslip Model
class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.DateField()
    basic_salary = models.DecimalField(max_digits=20, decimal_places=2)
    tax_deduction = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.net_salary = (
            self.basic_salary 
            + self.bonus 
            - self.tax_deduction 
            - self.other_deductions
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payroll for {self.employee.user.first_name} - {self.month.strftime('%B %Y')}"
