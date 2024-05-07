from django.shortcuts import render, get_list_or_404, get_object_or_404
from biometrics . models import Attendances
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext
from django.http import HttpResponseBadRequest
from datetime import  timedelta, time
import datetime
from collections import defaultdict
from django import forms
from django.template import RequestContext
from django.conf import settings
from .forms import SearchAttendanceForm, NonWorkingDaysForm
from .models import *
from django.forms.models import model_to_dict
from biometrics.models import Employee
from .forms import * 
import pandas as pd 
import os
from django.views.decorators.csrf import csrf_exempt
from dateutil import parser
import json
from django.core.serializers import serialize

# from django.http import QueryDict

# Create your views here.
class Payroll:
    def __init__(self, employee_info, attendances, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.employee_info = employee_info
        self.attendances = attendances
        self.timeInOut = self.compute_timeInOut()
        self.half_salary = self.employee_info['base_monthly_salary'] / 2
        self.working_days = self.get_workingDays(start_date, end_date)
        self.daily_pay = round(self.half_salary/len(self.working_days), 2)
        self.hourly_pay = round(self.daily_pay/8, 2)
        if self.employee_info['is_regular'] == True:
            self.daily_mealAllowance = 80.00
        else:
            self.daily_mealAllowance = 60.00
    def compute_mealAllowance(self):
        daily_mealAllowance = self.daily_mealAllowance
        meal_allowance = self.num_present_days * daily_mealAllowance
        return meal_allowance
    def compute_undertimeDeduct(self):
        num_undertime= self.num_undertime
        hourly_pay = self.hourly_pay
        undertime_deduct = num_undertime * float(hourly_pay)
        return round(undertime_deduct,2)
        
    def compute_tardinessDeduct(self):
        tardiness_time = self.num_tardinesstime
        tardiness_deduct = round((self.hourly_pay/60)*int(tardiness_time), 2)
        return tardiness_deduct
    
    def compute_overtimePay(self):
        overtime_hours = self.num_overtime
        overtime_pay = overtime_hours * (float(self.hourly_pay) * (125/100) )
        return round(overtime_pay, 2)
        # if overtime > datetime.timedelta(0):
    def get_workingDays(self, start_date, end_date):
        date_range = pd.date_range(start_date, end_date)
        days = ["Monday", "Tuesday", "Wednesday", 
        "Thursday", "Friday", "Saturday", "Sunday"] 
        working_days = []
        for single_date in date_range:
            if single_date.weekday() <5:
                working_days.append([single_date.strftime("%Y-%m-%d"), days[single_date.weekday()]])
        return working_days                 
    def compute_weekendPay(self):
        hourly_pay = self.hourly_pay
        weekend_work_hr = self.weekend_work_hr
        pay_multiplier = 150
        weekend_pay = weekend_work_hr * (float(hourly_pay) *(pay_multiplier/100))
        return round(weekend_pay,2)
    def compute_basicPay(self):
        working_days = self.working_days
        if self.employee_info['is_perfect_attendance'] == True or self.num_present_days == len(working_days):
            self.num_present_days = len(working_days)
            self.num_tardinesstime = 0
            basic_pay = self.half_salary
        else:
            daily_pay = self.daily_pay

            basic_pay = round(daily_pay * self.num_present_days, 2)
        
        return basic_pay 

    def compute_timeInOut(self):
        attendances = self.attendances
        dates = {}
        for attendance in attendances:
            if str(attendance['timestamp'].date()) not in dates:
                dates[str(attendance['timestamp'].date())] = []
            dates[str(attendance['timestamp'].date())].append(attendance)
        
        sorted_data = {}
        for date, data in dates.items():
            sorted_data[date] = sorted(data, key=lambda x: x['timestamp'])
        time_InOut ={}
        num_weekend_work_hr = datetime.timedelta(0)
        
        starting_time = time(hour=8,minute=1)
        ending_time = time(hour=17, minute=1)
        num_present_days = 0
        num_overtime = timedelta(0)
        num_tardinesstime = timedelta(0)
        num_undertime = timedelta(0)
        
        for date, data in sorted_data.items():
            week_day = datetime.datetime.strptime(date, "%Y-%m-%d").weekday()

            if week_day <5:
                
                time_InOut[date] = {}
                time_InOut[date]['in'] = data[0]['timestamp'].time()
                time_InOut[date]['out'] = None
                starting_timeObj = datetime.datetime.combine(datetime.date.today(), starting_time)
                in_timeObj = datetime.datetime.combine(datetime.date.today(), time_InOut[date]['in'])
                ending_timeObj= datetime.datetime.combine(datetime.date.today(), ending_time)
                
                if (datetime.datetime.combine(datetime.date.today(), data[-1]['timestamp'].time()) - in_timeObj) > timedelta(minutes=30):
                    num_present_days = num_present_days + 1
                    time_InOut[date]['out'] = data[-1]['timestamp'].time()
                    out_timeObj = datetime.datetime.combine(datetime.date.today(), time_InOut[date]['out'])
                
                    
                    if time_InOut[date]['in'] > starting_time:
                        time_InOut[date]['is_late'] = True
                        time_diff = in_timeObj - starting_timeObj 
                        time_InOut[date]['tardiness'] = time_diff
                        # print(f"{time_diff=}")
                        num_tardinesstime += time_diff
                    else:
                        time_InOut[date]['is_late'] = False

                    if time_InOut[date]['out'] == None:
                        time_InOut[date]['is_undertime'] = False
                        time_InOut[date]['is_overtime'] = False
                    else:
                        if time_InOut[date]['out'] < ending_time  :
                            time_InOut[date]['is_undertime'] = True
                            time_diff = ending_timeObj - out_timeObj
                            time_InOut[date]['undertime'] = time_diff
                            time_diff = ending_timeObj - out_timeObj
                            print(f"saa{ending_timeObj, out_timeObj}")
                            num_undertime += time_diff
                            print(f"{num_undertime= }")
                        else:
                            time_InOut[date]['is_undertime'] = False
                        
                        if time_InOut[date]['out'] > ending_time:
                            time_InOut[date]['is_overtime'] = True
                            time_diff = out_timeObj - ending_timeObj
                            time_InOut[date]['overtime'] = time_diff
                            num_overtime += time_diff
                        else:
                            time_InOut[date]['is_overtime'] = False
                            time_diff = ending_timeObj - out_timeObj
                            print(f"saa{ending_timeObj, out_timeObj}")
                            num_undertime += time_diff
                            print(f"{num_undertime= }")
                            
                else:
                    if time_InOut[date]['out'] == None:
                        del time_InOut[date]
            elif week_day == 5 or week_day == 6:
                print(datetime.date.today(), data[-1]['timestamp'].time(), datetime.date.today(), data[0]['timestamp'].time())
                time_diff = datetime.datetime.combine(datetime.date.today(), data[-1]['timestamp'].time()) - datetime.datetime.combine(datetime.date.today(), data[0]['timestamp'].time())
                
                num_weekend_work_hr = num_weekend_work_hr + time_diff
                days = ["Monday", "Tuesday", "Wednesday", 
                "Thursday", "Friday", "Saturday", "Sunday"] 
                print(date, days[week_day])
                print(date, date)
        # print(f"{weekend_work_hr=}")
        self.weekend_work_hr = self.seconds_to_hours(num_weekend_work_hr)
        self.num_undertime = self.seconds_to_hours(num_undertime)
        
        # print(num_present_days)
        self.num_present_days = num_present_days
        # self.num_overtime = num_overtime
        self.num_overtime = self.seconds_to_hours(num_overtime)
        self.num_tardinesstime = self.seconds_to_minutes(num_tardinesstime)
        return time_InOut
    def seconds_to_minutes(self,td):
        minutes = (td.total_seconds())/60
        return round(minutes,2)
    def seconds_to_hours(self, td):
        hours, remainder = divmod(td.total_seconds(), 3600)
        minutes = remainder/60
        hours_decimal = minutes/60
        # print(f"{hours_decimal=}")

        # formatted_time = f"{hours}:{minutes}:{seconds}"
        return round(hours+hours_decimal,2)



        


def salary(request):
    
    if request.method == 'POST':
        date_year = request.POST.get('date_year')
        month_half = request.POST.get('month_half')
        selected_year, selected_month = date_year.split('-')
        
        selected_year = int(selected_year)
        selected_month = int(selected_month)
        start_date = None
        end_date = None
        # print(f"{month_half=}")
        if month_half == '1':
            start_date = datetime.datetime(selected_year, selected_month, 1)
            end_date = datetime.datetime(selected_year, selected_month, 15)
        elif month_half == '2':
            start_date = datetime.datetime(selected_year, selected_month, 16)
            if selected_month == 12:
                selected_year = selected_year + 1
                selected_month = 1
            else:
                selected_month = selected_month + 1
            end_date =  datetime.datetime(selected_year, selected_month, 1) - datetime.timedelta(days=1)
            # days_in_month = datetime.datetime.replace(day=calendar.monthrange(date.year, date.month)[1]).day
            # last_day_of_previous_month = date.replace(day=days_in_month) - datetime.timedelta(days=1)
        # print(start_date)
        # print(end_date)
        
        records = list(Attendances.objects.filter(timestamp__range=[start_date, end_date], employee__is_registered = True).select_related('employee').order_by('-timestamp').values('timestamp', 'employee__dv_name', 'employee__dv_user_id', 'employee_id'))

        employee_list = list(Employee.objects.filter(is_registered = True).values())
        employee_attendance = {}
        
        for employee in employee_list:
            if employee['id'] not in employee_attendance:
                employee_attendance[employee['id']] = {}
            employee_attendance[employee['id']]['employee_info'] = employee
            if 'attendances' not in employee_attendance[employee['id']]:
                employee_attendance[employee['id']]['attendances']=[]
        for attendance in records:
            if attendance['employee_id'] not in employee_attendance:
                employee_attendance[attendance['employee_id']] = {}
            
            # if 'attendance' not in employee_attendance[attendance['employee_id']].keys():
            if 'attendances' not in employee_attendance[attendance['employee_id']]:
                employee_attendance[attendance['employee_id']]['attendance']=[]
            employee_attendance[attendance['employee_id']]['attendances'].append(attendance)
            
        employee_payroll = {}
        for employee_id, records in employee_attendance.items():
            # print(attendance)
            payroll = Payroll(records['employee_info'],records['attendances'],start_date, end_date)
            employee_payroll[employee_id] ={}
            employee_payroll[employee_id]['time_InOut']= payroll.timeInOut
            employee_payroll[employee_id]['employee_info'] = payroll.employee_info
            employee_payroll[employee_id]['basic_pay'] = payroll.compute_basicPay()
            employee_payroll[employee_id]['meal_allowance'] = payroll.compute_mealAllowance()
            employee_payroll[employee_id]['num_working_days'] = len(payroll.working_days)
            employee_payroll[employee_id]['working_days'] = payroll.working_days
            employee_payroll[employee_id]['num_present_days'] = payroll.num_present_days
            employee_payroll[employee_id]['overtime_pay'] = payroll.compute_overtimePay()
            employee_payroll[employee_id]['num_overtime'] = payroll.num_overtime
            employee_payroll[employee_id]['tardiness_deduct'] = payroll.compute_tardinessDeduct()
            employee_payroll[employee_id]['num_tardinesstime'] = payroll.num_tardinesstime
            employee_payroll[employee_id]['weekend_work_hr'] = payroll.weekend_work_hr
            employee_payroll[employee_id]['weekend_pay'] = payroll.compute_weekendPay()
            employee_payroll[employee_id]['num_undertime_hr'] = payroll.num_undertime
            employee_payroll[employee_id]['undertime_deduct'] = payroll.compute_undertimeDeduct()
            
            # print(f"{payroll.compute_undertimeDeduct()=}")
            # print(payroll.num_undertime, payroll.hourly_pay ,payroll.compute_undertimeDeduct())
            

        return JsonResponse({'records': employee_payroll})

    else:
        
        context = {
            'form': FilterSalaryForm(),
            'submit_form': PayrollForm()
        }        
        return render(request, 'hr/salary.html', context)

def index(request):
    return render(request, 'hr/index.html')
def attendances(request):
    context = {}
    context['form'] = SearchAttendanceForm()
    return render(request, 'hr/attendance.html', context)
def nonworking_days(request):
    context = {}
    context['form'] = NonWorkingDaysForm()
    return render(request, 'hr/nonworking_days.html', context)
def employees(request):
    context = {}
    context['form'] = EmployeeForm()
    return render(request, 'hr/employees.html', context)
def payroll(request):
    if request.method == 'POST':
        date_year = request.POST.get('date_year')
        month_half = request.POST.get('month_half')
        selected_year, selected_month = date_year.split('-')
        
        selected_year = int(selected_year)
        selected_month = int(selected_month)
        start_date = None
        end_date = None
        # print(f"{month_half=}")
        if month_half == '1':
            start_date = datetime.datetime(selected_year, selected_month, 1)
            end_date = datetime.datetime(selected_year, selected_month, 15)
        elif month_half == '2':
            start_date = datetime.datetime(selected_year, selected_month, 16)
            if selected_month == 12:
                selected_year = selected_year + 1
                selected_month = 1
            else:
                selected_month = selected_month + 1
            end_date =  datetime.datetime(selected_year, selected_month, 1) - datetime.timedelta(days=1)

        
        records = list(Payrolls.objects.filter(start_date=start_date, end_date = end_date, employee__is_registered = True).prefetch_related('employee').values(
            "employee__dv_user_id",
            "employee__last_name",
            "employee__first_name",
            "employee__position",
            "basic_pay", 
            "meal_allowance",
            "additional_pay",
            "overtime_pay",
            "tardiness_deduct",
            "leave_without_pay",
            "sss_contrib",
            "philhealth_contrib",
            "pagibig_contrib",
            "adjustment",
            'undertime_deduct',
            'weekend_pay',
            "id"
            ))
        # records = Payrolls.objects.filter(start_date=start_date, end_date=end_date, employee__is_registered=True).select_related('employee').all()

        # # Serialize queryset to JSON
        # json_records = serialize('json', records)
        # records_dict = json.loads(json_records)
        # context = {
        #     'records':records
        # }        
        print(records)
        return JsonResponse({"records":records}, safe = False)
    context = {
        'form': FilterSalaryForm(),
    }
    return render(request, 'hr/payroll.html', context)

def fetch_unregistered_employees(request):
    context = {}
    records = list(Employee.objects.values().filter(is_registered = False))
    context['records'] = records
    return JsonResponse(context, safe=False)
def register_employee(request, id):
    if request.method == 'POST':
        record = get_object_or_404(Employee, id = id)
        record.is_registered = True
        record.save()
        return JsonResponse({'success':'Success'})
def unregister_employee(request, id):
    # if request.method == 'POST':
    record = get_object_or_404(Employee, id = id)
    record.is_registered = False
    record.save()
    return JsonResponse({'success':'Success'})

def perfect_employee_attendance(request, id):
    # if request.method == 'POST':
    record = get_object_or_404(Employee, id = id)
    record.is_perfect_attendance = True
    record.save()
    return JsonResponse({'success':'Success'})
def imperfect_employee_attendance(request, id):
    # if request.method == 'POST':
    record = get_object_or_404(Employee, id = id)
    record.is_perfect_attendance = False
    record.save()
    return JsonResponse({'success':'Success'})
    

def fetch_employees(request):
    records = list(Employee.objects.values().filter(is_registered = True))
    
    return JsonResponse({'records': records}, safe=False)
def fetch_employee_detail(request, id):
    record = get_object_or_404(Employee, id = id)
    return JsonResponse(model_to_dict(record))
def update_employee(request, id):
    record = get_object_or_404(Employee, id = id)
    form  =  EmployeeForm(request.POST or None, instance= record)
    if form.is_valid():
        form.save()
    print(form.is_valid())
        
    return JsonResponse(model_to_dict(form.instance))

def delete_employee(request, id):
    record = get_object_or_404(Employee, id = id)
    record.delete()
    return JsonResponse({'message': 'Deleted successfully.'})


def download_attendances(request):
    records = list(Attendances.objects.select_related('employee').order_by('-timestamp').values('timestamp', 'employee__dv_name', 'employee__dv_user_id', 'employee_id'))
    dates = {}
    for r in records:
        if str(r['timestamp'].date()) not in dates:
            dates[str(r['timestamp'].date())] = []
        dates[str(r['timestamp'].date())].append(r)
            
    for id, logs in dates.items():
        employees = {}
        for log in logs:
            if log['employee_id'] not in employees:
                employees[log['employee_id']] = []
            employees[log['employee_id']].append(log)
        dates[id] = employees
        
    records = []
    for date, logs in dates.items():
        for x, log in logs.items():
            sorted_log = sorted(log, key=lambda x: x['timestamp'])

            time_in = sorted_log[0]['timestamp'].time()
            time_out = sorted_log[-1]['timestamp'].time()

            time_in_datetime = datetime.strptime(str(time_in), "%H:%M:%S")
            time_out_datetime = datetime.strptime(str(time_out), "%H:%M:%S")
            time_diff = time_out_datetime - time_in_datetime

            if time_diff < timedelta(minutes=30):
                time_out = None
            is_late = False
            is_overtime = False
            if time_in is not None and time_in > datetime.strptime('08:05:00', '%H:%M:%S').time():
                is_late = True
            if time_out is not None and time_out > datetime.strptime('17:05:00', '%H:%M:%S').time():
                is_overtime = True
                
            records.append({
                'date': date,
                'employee_id': x,
                'employee__dv_name': log[0]['employee__dv_name'],
                'employee__dv_user_id': log[0]['employee__dv_user_id'],
                'time_in': time_in,
                'time_out': time_out,    
                'is_late': is_late,
                'is_overtime': is_overtime,
            })
    df = pd.DataFrame(records)
    download_dir = r'C:\Users\CA\Downloads'
    download_path = os.path.join(download_dir, 'Attendance.xlsx')
    df.to_excel(download_path, index=False)

    return JsonResponse({'success': 'Success'})

def fetch_payroll_details(request, id):
    record = get_object_or_404(Payrolls, id=id)
    
    return JsonResponse(model_to_dict(record))
    
def submit_payroll(request, employee_id):
    if request.method == "POST":
        date_year = request.POST.get('date_year')
        month_half = request.POST.get('month_half')
        selected_year, selected_month = date_year.split('-')
        
        selected_year = int(selected_year)
        selected_month = int(selected_month)
        start_date = None
        end_date = None
        # print(f"{month_half=}")
        if month_half == '1':
            start_date = datetime.datetime(selected_year, selected_month, 1)
            end_date = datetime.datetime(selected_year, selected_month, 15)
        elif month_half == '2':
            start_date = datetime.datetime(selected_year, selected_month, 16)
            end_date =  datetime.datetime(selected_year, selected_month +1, 1) - datetime.timedelta(days=1)
            
        employee = get_object_or_404(Employee, id=employee_id)
        mutable_data = request.POST.copy()
        
        # Assign start_date and end_date to the mutable copy
        mutable_data['start_date'] = start_date
        mutable_data['end_date'] = end_date
        mutable_data['employee'] = employee
        
        
        # Pass the mutable copy to the form
        form = PayrollForm(mutable_data)
        
        # Manually clean and validate the form
        form.full_clean()
        if form.is_valid():
            # Assuming start_date and end_date are part of the form, update them in cleaned_data

            form.save()
            return JsonResponse({'success': 'Success'})
        else:
            return JsonResponse({'error': form.errors})

def add_attendances(request):
    if request.method == "POST":

        form = AttendanceForm(request.POST or None)
    
        if form.is_valid():
            form.save()
            return JsonResponse({'success': "Success"})

def fetch_attendances(request):
    records = list(Attendances.objects.select_related('employee').order_by('-timestamp').values('timestamp', 'employee__dv_name', 'employee__dv_user_id', 'employee_id').filter(employee__is_registered = True))
    
    dates = {}
    for r in records:
        if str(r['timestamp'].date()) not in dates:
            
            dates[str(r['timestamp'].date())] = []
        dates[str(r['timestamp'].date())].append(r)
    
    for id, logs in dates.items():
        employees = {}
        for log in logs:
            # print(log['timestamp'].date())
            if log['employee_id'] not in employees:
                employees[log['employee_id']] = []
            employees[log['employee_id']].append(log)
        dates[id] = employees
        
    records = []
    for date, logs in dates.items():
        for x, log in logs.items():
            sorted_log = sorted(log, key=lambda x: x['timestamp'])
            time_in = sorted_log[0]['timestamp'].time()
            time_out = sorted_log[-1]['timestamp'].time()

            time_in_datetime = datetime.datetime.strptime(str(time_in), "%H:%M:%S")
            time_out_datetime = datetime.datetime.strptime(str(time_out), "%H:%M:%S")
            time_diff = time_out_datetime - time_in_datetime

            if time_diff < timedelta(minutes=30):
                time_out = None
            is_late = False
            is_overtime = False
            if time_in is not None and time_in > datetime.datetime.strptime('08:05:00', '%H:%M:%S').time():
                is_late = True
            if time_out is not None and time_out > datetime.datetime.strptime('17:05:00', '%H:%M:%S').time():
                is_overtime = True
                
            records.append({
                'date':date,
                'employee_id':x,
                'employee__dv_name':log[0]['employee__dv_name'],
                'employe__dv_user_id':log[0]['employee__dv_user_id'],
                'time_in':time_in,
                'time_out':time_out,    
                'is_late': is_late,
                'is_overtime': is_overtime,
                })

    return JsonResponse({'records': records}, safe=True)


def add_nonworking_days(request):
    if request.method == "POST":

        form = NonWorkingDaysForm(request.POST or None)
    
        if form.is_valid():
            form.save()
    return JsonResponse({'success': "Success"})
def fetch_nonworking_days(request):
    records = list(NonWorkingDays.objects.values())
    for record in records:
        record['start'] = record['date']
        record['title'] = record['reason']
        del record['date']
        del record['reason']
    
    return JsonResponse(records, safe=False)

def compute_salary(request):
    base_salary = 4000.00
    

# def update_attendance(request, id):
#     record = get_object_or_404(Attendances, id = id)
#     form  =  AttendanceForm(request.POST or None, instance= record)
#     if form.is_valid():
#         form.save()
#     return JsonResponse(model_to_dict(form.instance))
# def delete_attendance(request, id):
#     record = get_object_or_404(Attendances, id = id)
#     record.delete()
#     return JsonResponse({'message': 'Deleted successfully.'})