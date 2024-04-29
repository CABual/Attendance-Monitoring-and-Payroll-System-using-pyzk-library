from django import forms
from .models import Employee, Attendances
from django.forms.widgets import DateTimeInput, Select


# creating a form
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
        ]
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