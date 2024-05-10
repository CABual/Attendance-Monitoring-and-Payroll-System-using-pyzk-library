from django import forms
from .models import Employee, Attendances, Device
from django.forms.widgets import DateTimeInput, Select, TextInput, NumberInput


# creating a form
class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = [
            'serial_number',
            'device_name',
            'ip_address',
            'port',
        ]

        widgets = {
            'serial_number': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ex. 1234567890',
                'disabled': 'true',
            }),
            'device_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ex. ZKTeco 8000',
                'disabled': 'true',
            }),
            'ip_address': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ex. 192.168.11.1',
                'disabled': 'true',
            }),            
            'port': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Default. 4370',
                'disabled': 'true',
            }),
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
            'base_monthly_salary',
            "civil_status",
            "gender",
            "mobile_number",
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
            'base_monthly_salary': NumberInput(attrs={
                'class': 'form-control',
                'oninput': 'this.value = Math.max(0, this.value)'
            })
        }
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