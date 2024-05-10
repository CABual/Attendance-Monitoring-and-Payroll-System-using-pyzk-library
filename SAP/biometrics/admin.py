from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Attendances)
admin.site.register(Device)
admin.site.register(Employee)
