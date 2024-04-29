from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from zk import ZK, const
from .models import Attendances, Employee
from django.core import serializers
from django.forms.models import model_to_dict
from . forms import EmployeeForm, AttendanceForm
from django.utils import timezone


# Create your views here.
def index(request):
    # return HttpResponse('hello, World')
    return render(request, 'biometrics/index.html')
def employees(request):
    return render(request, 'biometrics/employees.html')
def fetch_employees(request):
    records = list(Employee.objects.values())
    
    return JsonResponse({'records': records}, safe=False)
def fetch_employee_detail(request, id):
    record = get_object_or_404(Employee, id = id)
    return JsonResponse(model_to_dict(record))
def update_employee(request, id):
    record = get_object_or_404(Employee, id = id)
    form  =  EmployeeForm(request.POST or None, instance= record)
    if form.is_valid():
        form.save()
    return JsonResponse(model_to_dict(form.instance))

def delete_employee(request, id):
    record = get_object_or_404(Employee, id = id)
    record.delete()
    return JsonResponse({'message': 'Deleted successfully.'})

# def add_attendances(request):
#     con
def attendances(request):
    context = {}
    form = AttendanceForm()
    context['form'] = form
    # print("dsa")
    return render(request, 'biometrics/attendances.html', context)
def add_attendances(request):
    if request.method == "POST":

        form = AttendanceForm(request.POST or None)
    
        if form.is_valid():
            form.save()
    return JsonResponse({'success': "Success"})
def fetch_attendance_detail(request, id):
    record = get_object_or_404(Attendances, id = id)
    return JsonResponse(model_to_dict(record))
def update_attendance(request, id):
    record = get_object_or_404(Attendances, id = id)
    form  =  AttendanceForm(request.POST or None, instance= record)
    if form.is_valid():
        form.save()
    return JsonResponse(model_to_dict(form.instance))
def delete_attendance(request, id):
    record = get_object_or_404(Attendances, id = id)
    record.delete()
    return JsonResponse({'message': 'Deleted successfully.'})

def fetch_attendances(request):
    records = list(Attendances.objects.select_related('employee').values(
        'id', 'uid' , 'timestamp', 'status', 'punch', 'employee__dv_name', 'employee_id'
    ).order_by("-timestamp"))
    return JsonResponse({'records':records}, safe=False)

def download_employees(request):
    ip = '169.254.92.150'
    conn = None
    zk = ZK(ip, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
    
    try:
        conn = zk.connect()
        users = conn.get_users()
        saved_employees = list(Employee.objects.all().values_list('dv_user_id', flat= True))
        # print(saved_employees)
        for user in users:
            # print(user.user_id)
            
            if user.user_id in list(saved_employees):
                print(user.user_id)
                
                emp = Employee(user_id=user.user_id, name=user.name)
                emp.save()
                print(user.name)
                # print(user.user_id)
            else:
                emp = Employee.objects.filter(dv_user_id=user.user_id).update(dv_name=user.name)
                
        
    except Exception as e:
        print ("Process terminate : {}".format(e))
    
    finally:
        if conn:
            conn.disconnect()
    return JsonResponse('Success',safe=False)
def download_attendance(request): 
    
    # if request.method == 'POST':
        
    #     print(request.POST)
    #     return JsonResponse("heheh")
    ip = '169.254.92.150'
    conn = None
    zk = ZK(ip, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
    try:
        
        # connect to device
        conn = zk.connect()
        attendances = conn.get_attendance()
        att_map = {}
        saved_attendance = Attendances.objects.all().values_list('uid', flat= True)
        
        # for attendance in saved_attendance:
            
        for attendance in attendances:
            if(attendance.user_id not in att_map.keys()):
                att_map[attendance.user_id] = []
            if(attendance.uid not in saved_attendance):
                att_map[attendance.user_id].append(attendance)
                # print(attendance.timestamp)
        for employee, attend_obj in att_map.items():
            new_employee = Employee(dv_user_id=employee, dv_name=employee)
            new_employee.save()
            for attend in attend_obj:
                # new_attendance = Attendances(uid=attend.uid,
                #                          timestamp = attend.timestamp,
                #                          status = attend.status,
                #                          punch= attend.punch, 
                #                          employee = new_employee )
                # attend_timestamp = timezone.make_aware(attend.timestamp)
                print(attend.timestamp)
                new_attendance = Attendances(
                    uid=attend.uid,
                    timestamp=str(attend.timestamp),
                    status=attend.status,
                    punch=attend.punch,
                    employee=new_employee
                )
                new_attendance.save()
                
                
        conn.test_voice()
        conn.enable_device()
        
    except Exception as e:
        print ("Process terminate : {}".format(e))
    finally:
        if conn:
            conn.disconnect()
    return JsonResponse('Success', safe=False)

