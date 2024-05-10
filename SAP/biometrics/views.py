from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from zk import ZK, const
from .models import Attendances, Employee
from django.core import serializers
from django.forms.models import model_to_dict
from . forms import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def index(request):
    # return HttpResponse('hello, World')
    if request.method == "POST":

        form =DeviceForm(request.POST or None)

        if form.is_valid():
            form.save()
            latest_device = Device.objects.latest('id')
            device = model_to_dict(latest_device)
            return JsonResponse({'device':device })
    else:
        context = {
        }
        context['form'] = DeviceForm()
        
        return render(request, 'biometrics/index.html', context)
def try_device(request):
    device = Device.objects.latest('id')
    # ip = '169.254.92.150'
    # port = 4370
    ip = str(device.ip_address)
    port = int(device.port)
    
    print(f"{ip=}")
    print(f"{port=}")
    conn = None
    zk = ZK(ip, port=port, timeout=5, password=0, force_udp=False, ommit_ping=False)
    
    try:
        conn = zk.connect()
        users = conn.get_users()

        conn.disable_device()
                
        conn.test_voice(10)
        conn.test_voice(0)
        conn.enable_device() 
        return JsonResponse('Success: You can connect to this device!',safe=False)
    except Exception as e:
        print ("Process terminate : {}".format(e))
        return JsonResponse('Error: Please check your device configuration and try again.',safe=False)
    finally:
        if conn:
            conn.disconnect()
    # return JsonResponse('Success',safe=False)

def fetch_device(request):
    record = Device.objects.latest('id')
    return JsonResponse({'record': model_to_dict(record)}, safe=False)

@login_required
def employees(request):
    context = {}
    context['form'] = EmployeeForm()
    return render(request, 'biometrics/employees.html', context)
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
    print(form.is_valid())
        
    return JsonResponse(model_to_dict(form.instance))

def delete_employee(request, id):
    record = get_object_or_404(Employee, id = id)
    record.delete()
    return JsonResponse({'message': 'Deleted successfully.'})

# def add_attendances(request):
#     con
@login_required
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
    # print(form.is_valid())
    return JsonResponse(model_to_dict(form.instance))
def delete_attendance(request, id):
    record = get_object_or_404(Attendances, id = id)
    record.delete()
    return JsonResponse({'message': 'Deleted successfully.'})

def fetch_attendances(request):
    records = list(Attendances.objects.select_related('employee').values(
        'id', 'uid' , 'timestamp', 'overtime' , 'status', 'punch', 'employee__dv_name', 'employee_id'
    ).order_by("-timestamp"))
    return JsonResponse({'records':records}, safe=False)

def download_employees(request):
    device = Device.objects.latest('id')
    # ip = '169.254.92.150'
    # port = 4370
    ip = str(device.ip_address)
    port = int(device.port)
    
    print(f"{ip=}")
    print(f"{port=}")
    conn = None
    zk = ZK(ip, port=port, timeout=5, password=0, force_udp=False, ommit_ping=False)
    
    try:
        conn = zk.connect()
        users = conn.get_users()
        conn.disable_device()
        conn.test_voice(18)
        saved_employees = list(Employee.objects.all().values_list('dv_user_id', flat= True))
        # print(saved_employees)
        for user in users:
            # print(user.user_id)dsada
            if user.user_id in list(saved_employees):
                print(user.user_id)
                
                emp = Employee(user_id=user.user_id, name=user.name)
                emp.save()
                print(user.name)
                # print(user.user_id)
            else:
                emp = Employee.objects.filter(dv_user_id=user.user_id).update(dv_name=user.name)
                
        conn.test_voice()
        conn.enable_device() 
        return JsonResponse('Downloaded Successfully!',safe=False)
        
    except Exception as e:
        print ("Process terminate : {}".format(e))
        return JsonResponse('Error: Please check your device configuration and try again.',safe=False)

    finally:
        if conn:
            conn.disconnect()
    # return JsonResponse('Success',safe=False)
def download_attendance(request): 
    
    device = Device.objects.latest('id')
    # ip = '169.254.92.150'
    # port = 4370
    ip = str(device.ip_address)
    port = int(device.port)
    
    print(f"{ip=}")
    print(f"{port=}")
    conn = None
    zk = ZK(ip, port=port, timeout=5, password=0, force_udp=False, ommit_ping=False)
    try:
        
        # connect to device
        conn = zk.connect()
        conn.disable_device()
        conn.test_voice(18)
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
            try:
                new_employee = Employee(dv_user_id=employee, dv_name=employee)
                new_employee.save()
            except:
                new_employee = Employee.objects.get(dv_user_id=employee)
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
        return JsonResponse('Downloaded Successfully!',safe=False)
        
    except Exception as e:
        return JsonResponse('Error: Please check your device configuration and try again.',safe=False)
        
    finally:
        if conn:
            conn.disconnect()

