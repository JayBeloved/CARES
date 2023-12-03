import pandas as pd
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import Student

# Create your views here.
def home(request):
    return render(request, 'main/home.html')

def contribute(request):
    return render(request, 'main/contribute.html')

def access(request):
    return render(request, 'main/access.html')

def about(request):
    return render(request, 'main/about.html')

def verify(request):
    if request.method == "POST":
        # Get Matric Number
        MatricNo = request.POST.get('MatricNo')
        if MatricNo is None:
            messages.error(request, 'No Matric/Jamb Number')
            return HttpResponseRedirect(reverse("main:verify"))
        else:
            try:
                student = Student.objects.get(MatricNo=MatricNo)
                if student.Paid == 1:
                    # Payment is verified
                    return redirect('main:receipt', student_id=student.id)
                else:
                    messages.error(request, 'Payment Not Yet Verified, Try again later ')
                    return HttpResponseRedirect(reverse("main:verify")) 
            except ObjectDoesNotExist:
                messages.error(request, 'Something Went Wrong')
                return HttpResponseRedirect(reverse("main:verify"))
            
    return render(request, 'main/verify.html')

def receipt(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
        return render(request, 'main/receipt.html', {'student': student})
    except ObjectDoesNotExist:
        messages.error(request, 'Something Went Wrong')
        return HttpResponseRedirect(reverse("main:verify"))

# def import_excel(request):
#     if request.method == "POST" and request.FILES["csv_file"]:
#         data = request.FILES["csv_file"]

#         if data.name.endswith(".csv"):
#             # Read the Excel file using pandas
#             df = pd.read_csv(data)

#             # Loop through the DataFrame and create Student objects
#             for index, row in df.iterrows():
#                 student = Student(
#                     FullName=row["FullName"],
#                     MatricNo=row["MatricNo"],
#                     Level=row["Level"]
#                 )
#                 student.save()

#     return render(request, "main/import_excel.html")