from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import Group
class Employee(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    email=models.EmailField()
    contact = models.CharField(max_length=20)
    department = models.CharField(max_length=255)
    is_manager = models.BooleanField(default=False)
    username=models.CharField(max_length=255,unique=True)
    password=models.CharField(max_length=255)
    groups=models.ManyToManyField(Group)
    #user = models.OneToOneField(User, on_delete=models.CASCADE)


    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees',
        limit_choices_to={'is_manager': True}
    )

    def __str__(self):
        return self.name
    
    


    

class MyEmployee(Employee):
     class Meta:
          proxy=True
          
     def __str__(self):
         return self.name

