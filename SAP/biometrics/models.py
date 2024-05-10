from django.db import models

# Create your models here.
class Device(models.Model):
    serial_number = models.CharField(max_length=60, null=True)
    device_name = models.CharField(max_length=60, null=True)
    ip_address = models.CharField(max_length=50)
    port = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class Employee(models.Model):
    id = models.BigAutoField(primary_key=True)
    dv_user_id = models.BigIntegerField(unique=True)
    dv_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    middle_name = models.CharField(max_length=100, null=True)
    name_suffix = models.CharField(max_length=100, null=True)
    date_hired = models.DateField(null=True)
    birthday = models.DateField(null=True)
    birthplace = models.CharField(max_length=255, null=True)
    civil_status = models.CharField(max_length=25,null=True)
    gender = models.CharField(max_length=25, null=True)
    mobile_number = models.CharField(max_length=25, null=True)
    base_monthly_salary = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_regular = models.BooleanField(default=False)
    is_registered = models.BooleanField(default=False)
    is_perfect_attendance = models.BooleanField(default=False)


    def __str__(self):
        if(self.first_name == None):
            self.first_name = ""
        if(self.last_name == None):
            self.last_name = ""
        return f"{self.dv_name} -- {self.first_name}  {self.last_name}"
    
class Attendances(models.Model):
    id = models.BigAutoField(primary_key=True)
    uid  = models.BigIntegerField(null=True)
    timestamp = models.DateTimeField(max_length=50)
    status = models.IntegerField(null=True)
    punch = models.IntegerField(null=True)
    overtime = models.BooleanField(default=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    
    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "uid": self.uid,
    #         "timestamp": self.timestamp,
    #         "status": self.status,
    #         "punch": self.punch,
    #         "employee": self.employee.to_dict() if hasattr(self.employee, 'to_dict') else self.employee.__dict__,
    #         # ... add other attributes as needed ...
    #     }