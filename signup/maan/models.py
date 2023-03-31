from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=20)
    emergency_contact_name = models.CharField(max_length=255)
    

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=255)
    experience = models.IntegerField()
    education = models.CharField(max_length=255, default='')
   