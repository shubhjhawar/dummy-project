from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
# Create your models here.


status = (
        ('0', 'new'),
        ('1', 'in_progress'),
        ('2', 'hold'),
        ('3', 'complete'),
        ('4', 'reject'),
    )

user_status = (
        ('0', 'employee'),
        ('1', 'manager'),
)

class CustomUser(AbstractUser):
    user_status = models.CharField(max_length=20, choices=user_status, default='employee')
    objects = UserManager()
    REQUIRED_FIELDS = ['user_status']

    def __str__(self):
        return self.username

# class UserRegistrationModel(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=100)
#     username = models.CharField(max_length=35)
#     email = models.EmailField()
#     password = models.CharField(max_length=100)


class TaskModel(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(default=None)
    time = models.TimeField(default=None)
    user = models.ManyToManyField(CustomUser)
    location = models.CharField(max_length=500)
    amount = models.IntegerField()
    task_status = models.CharField(max_length=20, choices=status, default='new')

class APIKeyModel(models.Model):
    api_key = models.CharField(max_length=25)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)

class RemarkModel(models.Model):
    remark = models.CharField(max_length=500)
    task = models.ManyToManyField(TaskModel)


class ReasonModel(models.Model):
    reason_hold = models.CharField(max_length=500, null=True)
    reason_reject = models.CharField(max_length=500, null=True)
    task = models.ManyToManyField(TaskModel)
