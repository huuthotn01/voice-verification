# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    dob = models.DateField()

    class Meta:
        db_table = "user_info"

class UserVoice(models.Model):
    username = models.CharField(max_length=100)
    enroll_voice = models.CharField(max_length=100)

    class Meta:
        db_table = "user_voice"
        unique_together = (("username", "enroll_voice"),)