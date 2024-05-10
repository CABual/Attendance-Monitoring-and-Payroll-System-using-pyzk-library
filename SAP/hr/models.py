from django.db import models
from biometrics . models import Employee
# Create your models here.
class Events(models.Model):
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=True, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    # description = models.CharField(max_length=255, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.start_date} - {self.end_date}"
    
# class Salary(models.Model):
#     base_salary = models.FloatField()
#     overtime_salary = models.FloatField()
#     bonuses = models.FloatField()
#     total_compensation = models.FloatField()
#     total_deductions = models.FloatField()
#     total_salary = models.FloatField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
# class dede
class Payrolls(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    #earnings
    basic_pay = models.DecimalField(max_digits=10,decimal_places=2)
    meal_allowance = models.DecimalField(max_digits=10,decimal_places=2)
    additional_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overtime_pay = models.DecimalField(max_digits=10,decimal_places=2)
    weekend_pay = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    #earning multipliers
    weekend_work_hr = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    num_present_days = models.IntegerField()
    num_overtime_hr = models.DecimalField(max_digits=4, decimal_places=2)
    #deductions
    undertime_deduct = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    tardiness_deduct = models.DecimalField(max_digits=10,decimal_places=2,  default=0)
    leave_without_pay = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    sss_contrib = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    philhealth_contrib = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    pagibig_contrib = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    adjustment = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    #deduction multipliers        
    num_tardinesstime_min = models.DecimalField(max_digits=5, decimal_places=2)
    num_undertime_hr = models.DecimalField(max_digits=5, decimal_places=2,  default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    
    