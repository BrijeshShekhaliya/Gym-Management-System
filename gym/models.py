from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Enquiry(models.Model):
    name = models.CharField(max_length=20)
    contact = models.CharField(max_length=10)
    emailid = models.CharField(max_length=50)
    age = models.CharField(max_length=3)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=20)
    price = models.CharField(max_length=10)
    unit = models.CharField(max_length=10)
    date = models.CharField(max_length=40)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Plan(models.Model):
    name = models.CharField(max_length=20)
    amount = models.CharField(max_length=10)
    duration = models.CharField(max_length=3)


    def __str__(self):
        return self.name


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    contact = models.CharField(max_length=10)
    emailid = models.EmailField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    joindate = models.DateField()
    expiredate = models.DateField()
    initialamount = models.DecimalField(max_digits=10, decimal_places=2)
    submission_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Enquiry_Login(models.Model):
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    age = models.CharField(max_length=3)
    mobileno = models.CharField(max_length=10)
    emailid = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class VideoUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    streaming_url = models.URLField(blank=True, null=True)  # Add field for streaming URL
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
