from django import forms
from biometrics.models import  Attendances
from . models import NonWorkingDays
from django.forms.widgets import DateTimeInput, Select, TextInput


#
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