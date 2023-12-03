# import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Create variables to store user types
SUPER_ADMIN = 1
STUDENT = 2

USERTYPE_CHOICES = (
    (SUPER_ADMIN, 'Administrator'),
    (STUDENT, 'Student'), 
)

# Create variables to store payment status
PAID = 1
UNPAID = 0

PAYMENT_STATUS = (
    (PAID, 'Paid'),
    (UNPAID, 'Not-Paid'), 
)

class User(AbstractUser):
    # Add User type
    user_type = models.PositiveSmallIntegerField(choices=USERTYPE_CHOICES, default=STUDENT)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'user_type']


# Model for landlords
class Student(models.Model):
    FullName = models.CharField(max_length=100, null=True)
    MatricNo = models.CharField(max_length=30, null=True, blank=True)
    Level = models.CharField(max_length=15, null=True, blank=True)
    Paid = models.PositiveSmallIntegerField(choices=PAYMENT_STATUS, default=UNPAID)
    Amount = models.FloatField('Amount Paid', max_length=40, null=True, blank=True)
    Date = models.DateField('Payment Date', default=timezone.now, null=True, blank=True)
    ReceiptNo = models.CharField(max_length=30, unique=True, null=True, blank=True)

    def __str__(self):
        return self.FullName
    
