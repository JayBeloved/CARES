# import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Create variables to store user types
SUPER_ADMIN = 1
STUDENT = 2
ACADEMIC = 3

USERTYPE_CHOICES = (
    (SUPER_ADMIN, 'Administrator'),
    (ACADEMIC, 'Academic Officer'),
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


# Model for Students
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

# Model for Courses    
class Course(models.Model):
    course_title = models.CharField(max_length=255)
    course_code = models.CharField(max_length=20)
    level = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.code} ({self.title})"

# Model for resources
class Resource(models.Model):
    CATEGORY_CHOICES = [
        ('material', 'Course Material'),
        ('pq', 'Past Question'),
        ('solution', 'Suggested Solution'),
        ('ican', 'ICAN')
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    mat_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    resource_code = models.CharField(max_length=30, unique=True, null=True, blank=True)
    date_added = models.DateField('Upload Date', default=timezone.now, null=True, blank=True)
    link = models.URLField()

    def __str__(self):
        return f"{self.category} - {self.name} ({self.course.course_code})"