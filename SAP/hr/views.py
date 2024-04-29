from django.shortcuts import render
from biometrics . models import Attendances
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext
from django.http import HttpResponseBadRequest
from datetime import datetime, timedelta
from collections import defaultdict
from django import forms
from django.template import RequestContext
from django.conf import settings
from .forms import SearchAttendanceForm, NonWorkingDaysForm
from .models import NonWorkingDays
from django.forms.models import model_to_dict

import pandas as pd 
import os

# Create your views here.
def index(request):
    # return HttpResponse('hello, World')
    return render(request, 'hr/index.html')
def attendances(request):
    context = {}
    context['form'] = SearchAttendanceForm()
    return render(request, 'hr/attendance.html', context)


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
                'employe__dv_user_id': log[0]['employee__dv_user_id'],
                'time_in': time_in,
                'time_out': time_out,    
                'is_late': is_late,
                'is_overtime': is_overtime,
            })
    df = pd.DataFrame(records)
    download_dir = r'C:\Users\CA\Downloads'
    download_path = os.path.join(download_dir, 'Attendance.xlsx')
    df.to_excel(download_path, index=False)
    # print(df)
    
    # excel_file = pd.ExcelWriter('employee_data.xlsx', engine='xlsxwriter')
    # df.to_excel(excel_file, index=False)
    # excel_file.save()
    return JsonResponse({'success': 'Success'})

    # sheet = excel.pe.sheet(records)
    # return excel.make_response(sheet, "csv")
def fetch_attendances(request):
    # records = list(Attendances.objects.select_related('employee').values('timestamp', 'status', 'punch', 'employee__dv_name', 'employee_id'))
    records = list(Attendances.objects.select_related('employee').order_by('-timestamp').values('timestamp', 'employee__dv_name', 'employee__dv_user_id', 'employee_id'))
    # for r in records:
    #     print(r)
    # time_records = defaultdict(list)

    # # Sort the records by timestamp
    # sorted_records = sorted(records, key=lambda x: x['timestamp'])

    # # Iterate through records
    # for i in range(0, len(sorted_records), 2):
    #     time_in_record = sorted_records[i]
    #     time_out_record = sorted_records[i+1] if i+1 < len(sorted_records) else None

    #     # Add time in and time out to the time_records dictionary
    #     time_records[time_in_record['employee_id']].append((time_in_record['timestamp'], time_out_record['timestamp']))

    # # Print the time in and time out for each employee
    # for employee_id, times in time_records.items():
    #     print(f"\n\nEmployee ID: {employee_id}")
    #     print(times)
    #     for time_in, time_out in times:
    #         print(f"  Time In: {time_in}, Time Out: {time_out}")   
    # print(records)
    # employees = {}
    # for r in records:
    #     if r['employee_id'] not in employees:
    #         employees[r['employee_id']] = []
    #     employees[r['employee_id']].append(r)
    
    # # employee_
    
    # for id, logs in employees.items():
    #     # print(id, len(logs))
    #     date = {}
    #     for log in logs:
    #         # print(log['timestamp'].date())
    #         if str(log['timestamp'].date()) not in date:
    #             date[str(log['timestamp'].date())] = []
    #         date[str(log['timestamp'].date())].append(log)
    #     employees[id] = date
    # for id, logs in employees.items():
    #     print(id)  
    #     for x, log in logs.items():
    #         print(x)
    #         print(log)
    
    dates = {}
    for r in records:
        if str(r['timestamp'].date()) not in dates:
            
            dates[str(r['timestamp'].date())] = []
        dates[str(r['timestamp'].date())].append(r)
            
    
    # employee_
    
    for id, logs in dates.items():
        # print(id, len(logs))
        employees = {}
        for log in logs:
            # print(log['timestamp'].date())
            if log['employee_id'] not in employees:
                employees[log['employee_id']] = []
            employees[log['employee_id']].append(log)
        dates[id] = employees
        
    records = []
    for date, logs in dates.items():
        # print(date)  
        for x, log in logs.items():
            # time_in = None
            sorted_log = sorted(log, key=lambda x: x['timestamp'])

            # print(x)
            # print(log)
            # time_out = None
            time_in = sorted_log[0]['timestamp'].time()
            time_out = sorted_log[-1]['timestamp'].time()

            time_in_datetime = datetime.strptime(str(time_in), "%H:%M:%S")
            time_out_datetime = datetime.strptime(str(time_out), "%H:%M:%S")
            time_diff = time_out_datetime - time_in_datetime

            # Check if the time difference is less than 30 minutes
            if time_diff < timedelta(minutes=30):
                time_out = None
            is_late = False
            is_overtime = False
            if time_in is not None and time_in > datetime.strptime('08:05:00', '%H:%M:%S').time():
                is_late = True
            if time_out is not None and time_out > datetime.strptime('17:05:00', '%H:%M:%S').time():
                is_overtime = True
                # if log{'timestamp'}.time()  < datetime.strptime('08:00:00', '%H:%M:%S').time():
                
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
            # print(x)
            # print(log)
    
        # for d, r in date.items():
        #     print(d, r)
            # print(r)
        # print(r['timestamp'])
    # return JsonResponse({'records': employees}, safe=True)
    return JsonResponse({'records': records}, safe=True)

def nonworking_days(request):
    context = {}
    context['form'] = NonWorkingDaysForm()
    return render(request, 'hr/nonworking_days.html', context)
def add_nonworking_days(request):
    if request.method == "POST":

        form = NonWorkingDaysForm(request.POST or None)
    
        if form.is_valid():
            form.save()
    return JsonResponse({'success': "Success"})
def fetch_nonworking_days(request):
    # records = NonWorkingDays.objects.all()
    records = list(NonWorkingDays.objects.values())
    for record in records:
        record['start'] = record['date']
        record['title'] = record['reason']
        del record['date']
        del record['reason']
        

        print(record)
        # record = record.rename({'date': 'start'})
    
    return JsonResponse(records, safe=False)
    # return JsonResponse(model_to_dict(records))
# def add_attendances(request):
#     if request.method == "POST":

#         form = AttendanceForm(request.POST or None)
    
#         if form.is_valid():
#             form.save()
#     return JsonResponse({'success': "Success"})
# def fetch_attendance_detail(request, id):
#     record = get_object_or_404(Attendances, id = id)
#     return JsonResponse(model_to_dict(record))
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