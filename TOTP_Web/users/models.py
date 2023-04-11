from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class OTP(models.Model):
    otp = models.CharField(default='', max_length=15, verbose_name='otp')
    user_id = models.IntegerField(verbose_name='user_id', unique=True)
    serial = models.CharField(default ='', max_length=10, verbose_name='serial', unique=True)

