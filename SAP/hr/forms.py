from django import forms
from biometrics.models import  Attendances
from . models import NonWorkingDays, Payrolls
from django.forms.widgets import DateTimeInput, DateInput, Select, TextInput, NumberInput,SelectDateWidget, CheckboxInput
from .widgets import MonthYearWidget
from biometrics.models import Employee, Attendances
from datetime import date
class FilterSalaryForm(forms.Form):
    
    half_choices= ((1, 'First Cut-off'),(2, 'Second Cut-off'),)
    date_year = forms.DateField(widget=DateInput(attrs={
        'type': 'month',
        'class': 'form-control',
        'value': date.today().strftime("%Y-%m")
    }), initial=date.today().strftime("%Y-%m"))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = date.today()
        if today.day >= 16:
            self.fields['month_half'].initial = 2
        else:
            self.fields['month_half'].initial = 1

    month_half = forms.ChoiceField(choices=half_choices, widget=Select(attrs={
        'class': 'form-select'
    }))

class AttendanceForm(forms.ModelForm):
    class Meta:
        # specify model to be used
        model = Attendances
        # specify fields to be used
        fields = [
            "timestamp",
            "employee",
        ]
        widgets = {
            'timestamp': DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'employee': Select(attrs={
                'class': 'form-select'
            })
        }
        
class EmployeeForm(forms.ModelForm):

	# create meta class
    class Meta:
        # specify model to be used
        model = Employee
        # specify fields to be used
        fields = [
            "position",
            "last_name",
            "first_name",
            "middle_name",
            "name_suffix",
            "birthday",
            "date_hired",
            "birthplace",
            "civil_status",
            "gender",
            "mobile_number",
            "is_regular",
            'base_monthly_salary',
        ]
        widgets = {
            'position': TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control'
            }),
            'first_name': TextInput(attrs={
                'class': 'form-control'
            }),
            'middle_name': TextInput(attrs={
                'class': 'form-control'
            }),
            'name_suffix': TextInput(attrs={
                'class': 'form-control',
                'required': 'false'
            }),
            'birthday': DateTimeInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'date_hired': DateTimeInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'birthplace': TextInput(attrs={
                'class': 'form-control'
            }),
            'civil_status': Select(attrs={
                'class': 'form-select'
            }, choices=[('SINGLE', 'SINGLE'), ('MARRIED', 'MARRIED'), ('SEPARATED', 'SEPARATED')]),
            'gender': Select(attrs={
                'class': 'form-select'
            }, choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')]),
            'mobile_number': NumberInput(attrs={
                'class': 'form-control',
            }),
            'is_regular': CheckboxInput(attrs={
                'class': 'form-input'
            }),
            'base_monthly_salary': NumberInput(attrs={
                'class': 'form-control',
                'oninput': 'this.value = Math.max(0, this.value)'
            })
        }

class SearchAttendanceForm(forms.ModelForm):
    class Meta:
        # specify model to be used
        model = Attendances
        # specify fields to be used
        fields = [
            "timestamp",
            "employee",
        ]
        widgets = {
            'timestamp': DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'required': 'false'
            }),
            'employee': Select(attrs={
                'class': 'form-select',
                'required': 'false'
                
            })
        }
class NonWorkingDaysForm(forms.ModelForm):

    class Meta:
        model = NonWorkingDays
        fields =[
            'date',
            'reason'
        ]
        widgets = {
            'date': DateTimeInput(attrs={
                'type': 'date',
                'class': 'form-control',
                # 'required': 'false'
            }),
            'reason': TextInput(attrs={
                'class': 'form-control',
                # 'required': 'false'
            })
        }
class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payrolls
        # fields = ['basic_pay', '']
        exclude = [
            'created_at', 
            'updated_at'
        ]

        widgets = {
            'weekend_work_hr': TextInput(attrs={
                'class': 'form-control',
                'readonly': 'True'
            }),
            'weekend_pay': TextInput(attrs={
                'class': 'form-control earnings',
                'readonly': 'True'
            }),
            'num_undertime_hr': TextInput(attrs={
                'class': 'form-control',
                'readonly': 'True'
            }),
            'undertime_deduct': TextInput(attrs={
                'class': 'form-control deductions',
                'readonly': 'True'
            }),
            'basic_pay': TextInput(attrs={
                'class': 'form-control earnings',
                'readonly': 'True'
            }),
            'meal_allowance': TextInput(attrs={
                'class': 'form-control earnings',
                'readonly': 'True'
            }),
            'overtime_pay': TextInput(attrs={
                'class': 'form-control earnings',
                'readonly': 'True'
            }),
            'additional_pay': NumberInput(attrs={
                'class': 'form-control earnings',
                # 'required': 'false'
            }),
            'num_present_days': TextInput(attrs={
                'class': 'form-control',
                'readonly': 'True'
            }),            
            'num_overtime_hr': TextInput(attrs={
                'class': 'form-control',
                'readonly': 'True'
            }),            
            'tardiness_deduct': TextInput(attrs={
                'class': 'form-control deductions',
                'readonly': 'True'
            }),            
            'leave_without_pay': NumberInput(attrs={
                'class': 'form-control deductions',
                # 'required': 'false'
            }),
            'sss_contrib': NumberInput(attrs={
                'class': 'form-control deductions',
                # 'required': 'false'
            }),
            'philhealth_contrib': NumberInput(attrs={
                'class': 'form-control deductions',
                # 'required': 'false'
            }),
            'pagibig_contrib': NumberInput(attrs={
                'class': 'form-control deductions',
                # 'required': 'false'
            }),
            'adjustment': NumberInput(attrs={
                'class': 'form-control deductions',
                # 'required': 'false'
            }),
            'num_tardinesstime_min': TextInput(attrs={
                'class': 'form-control',
                'readonly': 'True'
            }),
        }