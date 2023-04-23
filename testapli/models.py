import email
from email.headerregistry import Address
from unicodedata import name
from django.db import models

# Create your models here.
class student(models.Model):
    roll=models.CharField(max_length=100)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=150)
    address=models.CharField(max_length=200)
    phone=models.CharField(max_length=10)
