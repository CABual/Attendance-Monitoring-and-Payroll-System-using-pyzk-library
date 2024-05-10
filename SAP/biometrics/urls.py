from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("device/fetch/latest", views.fetch_device),
    path("device/try/", views.try_device),
    path("download/attendance/", views.download_attendance, name="download_attendance"),
    path("download/employees/", views.download_employees, name="download_employees"),
    path("employees/", views.employees, name="employees"),
    path("employees/fetch/", views.fetch_employees, name="fetch_employees"),
    path("employees/fetch/<int:id>/", views.fetch_employee_detail, name=""),
    path("employees/delete/<int:id>/", views.delete_employee, name=""),
    path("employees/update/<int:id>/", views.update_employee),
    path("attendances/", views.attendances, name="employees"),
    path("attendances/fetch/", views.fetch_attendances, name="fetch_attendances"),
    path("attendances/add/", views.add_attendances, name=""),
    path("attendances/fetch/<int:id>/", views.fetch_attendance_detail, name=""),
    path("attendances/update/<int:id>/", views.update_attendance),
    path("attendances/delete/<int:id>/", views.delete_attendance),
    
]
