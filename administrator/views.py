import random, string
import numpy as np
import pandas as pd
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

########################

from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
from main.models import Student


# Create your views here.
def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_type == 1:
                    return redirect("administrator:dashboard")
                    # return HttpResponse("ADMIN DASHBOARD")
                elif user.user_type == 2:
                    messages.success(request, 'STUDENT SUCCESSFUL LOGIN')
                    # return redirect("agents:dashboard")
                    return HttpResponse("STUDENT DASHBOARD")
                else:
                    msg = 'Something Went Wrong'
                    HttpResponseRedirect('landing')
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "administrator/login.html", {"form": form, "msg": msg})


def login_redirect(request):
    return HttpResponseRedirect('login')

@login_required
def dashboard(request):
    # Check if there are students in the database
    check = len(Student.objects.all())
    if check > 0:
        # Get all rentals
        allstudents = Student.objects.all()
        # Create DataFrame of all Rental Agreements
        df = pd.DataFrame.from_records(allstudents.values())

        # Convert date ending and date started to datetime datatype
        df[['Date']] = df[['Date']].apply(pd.to_datetime)
        df[['Level']] = df[['Level']].apply(pd.to_numeric)


        # Get values 
        all_students,_ = df.shape
        amount_paid = df['Amount'].sum()
        
        df_paid = df[df['Paid']==1] # Data of students that have paid
        df_unpaid = df[df['Paid']==0] # Data of students that have not paid
        no_paid, _ = df_paid.shape # Number of students that have paid
        no_unpaid, _ = df_unpaid.shape # Number of students that have not paid
        perc_paid = np.round((no_paid/all_students)*100,2)

        # Convert the 

        """
        Values for Payment Progress
        
        """
        # 400 Level
        df_400 = df[df['Level']==400]
        df_400_paid = df_400[df_400['Paid']==1]
        no_400,_ = df_400.shape
        no_400_paid,_ = df_400_paid.shape
        if no_400 > 0:
            perc_400 = np.round((no_400_paid/no_400 * 100), 2)
        else:
            perc_400 = 0

        # 300 Level
        df_300 = df[df['Level']==300]
        df_300_paid = df_300[df_300['Paid']==1]
        no_300,_ = df_300.shape
        no_300_paid,_ = df_300_paid.shape
        if no_300 > 0:
            perc_300 = np.round((no_300_paid/no_300 * 100), 2)
        else:
            perc_300 = 0

        # 200 Level
        df_200 = df[df['Level']==200]
        df_200_paid = df_200[df_200['Paid']==1]
        no_200,_ = df_200.shape
        no_200_paid,_ = df_200_paid.shape
        if no_200 > 0:
            perc_200 = np.round((no_200_paid/no_200 * 100), 2)
        else:
            perc_200 = 0

        # 100 Level
        df_100 = df[df['Level']==100]
        df_100_paid = df_100[df_100['Paid']==1]
        no_100,_ = df_100.shape
        no_100_paid,_ = df_100_paid.shape
        if no_100 > 0:
            perc_100 = np.round((no_100_paid/no_100 * 100), 2)
        else:
            perc_100 = 0




    context = {
        'all_students':all_students,
        'amount_paid':amount_paid,
        'perc_paid':perc_paid,
        'no_unpaid': no_unpaid,
        'perc_400': perc_400,
        'perc_300': perc_300,
        'perc_200': perc_200,
        'perc_100': perc_100,
    }

    return render(request, 'administrator/dashboard/dashboard.html', context) 

class StudentsListView(ListView):
    model = Student
    template_name = "administrator/dashboard/students.html"
    context_object_name = "students"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.user_type == 1:
            # Get all students
            queryset = Student.objects.all()
        return queryset

    # extra_context = {
    #     'alertCount': alert()[1],
    #     'alerts': alert()[0],
    # }
    ordering = ['-id']
    paginate_by = 10

@login_required
def verify(request, student_id):
    if student_id is None:
        messages.error(request, 'No Student Selected')
        return HttpResponseRedirect(reverse("administrator:students"))
    else:
        try:
            student = Student.objects.get(id=student_id)
        except ObjectDoesNotExist:
            messages.error(request, 'Something Went Wrong')
            return HttpResponseRedirect(reverse("administrator:students"))
    
    form = StudentVerificationForm(request.POST or None)
    
    # Check for form submission
    if request.method == "POST":
        # Check form submission
        if form.is_valid():
            payment_date = form.cleaned_data.get("Date")
            amount = form.cleaned_data.get("Amount")
            status = form.cleaned_data.get("Paid")

            # Generate Unique ReceiptNo
            #############################
            # Randomly Choose Letters for adding to code
            def gencode():
                char1 = random.choice(string.ascii_uppercase)
                char2 = random.choice(string.ascii_lowercase)
                char3 = random.choice(string.ascii_letters)
                char4 = random.choice('1234567890')

                return f"RUNASA/2023/{student_id}/{char1}{char2}{char4}{char3}"

            #############################
            rcn = gencode()
            receipt_no = rcn
            while Student.objects.filter(ReceiptNo=rcn):
                rcn = gencode()
                if not Student.objects.filter(receipt_no=gencode):
                    receipt_no = gencode
            
            # Update the Student Record
            student.Paid, student.Amount, student.Date, student.ReceiptNo = (status,amount,payment_date,receipt_no)
            student.save()
            
            messages.success(request, 'Payment Verified Successfully')
            return HttpResponseRedirect(reverse("administrator:students"))

    context = {
        'student': student,
        'form': form,
    }

    return render(request, 'administrator/dashboard/verification.html', context)


@login_required()
def search(request):
    # Default assignment for querysets
    students = None
    query = None
    count = 0

    if request.method == 'GET':
        query = request.GET.get('q')
        if query is None:
            messages.error(request, 'Empty Search')
            return HttpResponseRedirect(reverse("administrator:dashboard"))
        else:
            query_clean = query.replace(" ", "+")
            query = query.upper()
            try:
                # Filter students to get matches
                students = Student.objects.filter(MatricNo__contains=query)
                count = len(students)
            except ObjectDoesNotExist:
                messages.error(request, 'Empty Search')
                return HttpResponseRedirect(reverse("administrator:dashboard"))

    context = {
        'students': students,
        'count': count,
        'query': query,
    }

    return render(request, 'administrator/dashboard/search.html', context)
    
# @login_required
# def update(request, student_id):
#     if student_id is None:
#         messages.error(request, 'No Student Selected')
#         return HttpResponseRedirect(reverse("administrator:students"))
#     else:
#         try:
#             student = Student.objects.get(id=student_id)
#         except ObjectDoesNotExist:
#             messages.error(request, 'Something Went Wrong')
#             return HttpResponseRedirect(reverse("administrator:students"))
    
    