from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("events/", views.events, ),
    path("events/add/", views.add_events, name=""),
    path("events/fetch/", views.fetch_events, name=""),
    path("events/delete/<int:id>/", views.delete_events, name=""),
    path('employees/', views.employees),
    path('employees/register/<int:id>/', views.register_employee),
    path('employees/unregister/<int:id>/', views.unregister_employee),
    path('employees/perfect/attendance/<int:id>/', views.perfect_employee_attendance),
    path('employees/imperfect/attendance/<int:id>/', views.imperfect_employee_attendance),
    path("employees/fetch/", views.fetch_employees, name="fetch_employees"),
    path("employees/fetch/<int:id>/", views.fetch_employee_detail, name=""),
    path("employees/delete/<int:id>/", views.delete_employee, name=""),
    path("employees/update/<int:id>/", views.update_employee),
    path("employees/unregistered/fetch/", views.fetch_unregistered_employees, name=""),
    # path("employees/compute-salary", views.compute_salary),
    path("attendances/fetch/", views.fetch_attendances, name=""),
    path("attendances/download/", views.download_attendances, name=""),
    path("attendances/", views.attendances, name=""),
    path("attendances/add/", views.add_attendances, name=""),
    path("payroll/submit/<int:employee_id>/", views.submit_payroll, name=""),
    path("payroll/fetch/<int:id>/", views.fetch_payroll_details),
    path("salary/", views.salary, name=""),
    path("payroll/", views.payroll,),
    path('payroll/delete/<int:id>/', views.delete_payroll), 


]