from django.contrib import admin
from emsa import models
from .models import Employee,MyEmployee
# Register your models here.
admin.site.register(Employee)
admin.site.register(MyEmployee)