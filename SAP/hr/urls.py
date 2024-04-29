from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("non-working-days/", views.nonworking_days, name="nonworking_days"),
    path("non-working-days/add/", views.add_nonworking_days, name=""),
    path("non-working-days/fetch/", views.fetch_nonworking_days, name=""),

    path("attendances/fetch/", views.fetch_attendances, name=""),
    path("attendances/download/", views.download_attendances, name=""),
    
    path("attendances/", views.attendances, name=""),

]