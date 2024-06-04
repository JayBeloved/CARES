import random, string
import numpy as np
import pandas as pd
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

########################

from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
from main.models import Student, Course, Resource

# Create a function that export the tables in the database to an excel file
def export_excel(request):
    students = Student.objects.all()
    student_df = pd.DataFrame.from_records(students.values())

    # Convert the DataFrame to a CSV file
    csv_file = student_df.to_csv(index=False)

     # Create a HttpResponse object with the csv file content
    response = HttpResponse(csv_file, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=students.csv'

    return response


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
                elif user.user_type == 3:
                    return redirect("administrator:edu_dashboard")
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
def edu_dashboard(request):
    # Check if there are resources in the database
    all_resources, course_materials, past_questions, ican, solution = (0,0,0,0,0)
    courses = []
    categories = []
    recent_mat = []
    recent_pq = []
    check = len(Resource.objects.all())
    if check > 0:
        # Get all resources
        allresources = Resource.objects.all()
        # Create DataFrame of all resources
        df = pd.DataFrame.from_records(allresources.values())

        # Convert date to numeric
        df[['date_added']] = df[['date_added']].apply(pd.to_datetime)


        # Get values 
        all_resources,_ = df.shape
        
        df_materials = df[df['category']=='material'] # Data of course materials
        df_pq = df[df['category']=='pq'] # Data of past questions
        df_ican = df[df['category']=='ican'] # Data of ican materials
        df_solutions= df[df['category']=='solution'] # Data of suggested solutions
        
        # Get Counts
        course_materials, _ = df_materials.shape # Number course materials
        past_questions, _ = df_pq.shape # Number of past questions
        ican, _ = df_ican.shape # Number of ican materials
        solution, _ = df_solutions.shape

        # Get the recently added metarials
        recent_mat = Resource.objects.filter(category='material').order_by('-date_added')[:5]

        # Get the recently added past questions
        recent_pq = Resource.objects.filter(category='pq').order_by('-date_added')[:5]

        # Get the course list
        courses = Course.objects.all()

        # Get Categories List
        categories = {
        'material': 'Course Material',
        'pq': 'Past Question',
        'solution': 'Suggested Solution',
        'ican': 'ICAN'
    }

    context = {
        'all_resources':all_resources,
        'course_materials':course_materials,
        'past_questions':past_questions,
        'ican': ican,
        'solution': solution,
        'recent_mat': recent_mat,
        'recent_pq': recent_pq,
        'courses': courses,
        'categories': categories,
    }

    return render(request, 'administrator/dashboard/educator_dash.html', context) 


@login_required
def dashboard(request):
    # Check if there are students in the database
    all_students = 0
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
    paginate_by = 25


class ResourcesListView(ListView):
    model = Resource
    template_name = "administrator/dashboard/resources.html"
    context_object_name = "resources"

    # Get the course list
    courses = Course.objects.all()

    # Get Categories List
    categories = {
    'material': 'Course Material',
    'pq': 'Past Question',
    'solution': 'Suggested Solution',
    'ican': 'ICAN'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.user_type == 1:
            # Get all resources
            queryset = Resource.objects.all()
        return queryset

    extra_context = {
        'courses': courses,
        'categories': categories,
    }
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


from django.utils import timezone

@login_required
def verify_multiple(request):
    student_ids = request.POST.getlist('student_ids')
    for student_id in student_ids:
        try:
            student = Student.objects.get(id=student_id)
        except ObjectDoesNotExist:
            messages.error(request, 'Something Went Wrong')
            return HttpResponseRedirect(reverse("administrator:students"))

        # Set the payment details
        payment_date = timezone.now()
        amount = 10000
        status = 'Paid'

        # Generate Unique ReceiptNo
        def gencode():
            char1 = random.choice(string.ascii_uppercase)
            char2 = random.choice(string.ascii_lowercase)
            char3 = random.choice(string.ascii_letters)
            char4 = random.choice('1234567890')

            return f"RUNASA/2023/{student_id}/{char1}{char2}{char4}{char3}"

        rcn = gencode()
        receipt_no = rcn
        while Student.objects.filter(ReceiptNo=rcn):
            rcn = gencode()
            if not Student.objects.filter(receipt_no=gencode):
                receipt_no = gencode

        # Update the Student Record
        student.Paid, student.Amount, student.Date, student.ReceiptNo = (status,amount,payment_date,receipt_no)
        student.save()

        messages.success(request, f'Payment for student {student_id} Verified Successfully')

    return render(request, 'administrator/dashboard/multiple.html')


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
                students = Student.objects.filter(
                    Q(MatricNo__contains=query) | 
                    Q(FullName__icontains=query)  # Add this line
                )
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


@login_required()
def upload_resource(request):
    # Create view function to upload resources
    form = ResourceUploadForm(request.POST or None)
    cat = ""
    # Get the course list
    courses = Course.objects.all()

    # Get Categories List
    categories = {
    'material': 'Course Material',
    'pq': 'Past Question',
    'solution': 'Suggested Solution',
    'ican': 'ICAN'
    }
    # Check for form submission
    if request.method == "POST":
        # Check form submission
        if form.is_valid():
            # Get the form fields
            course = form.cleaned_data.get('course')
            category = form.cleaned_data.get('category')
            mat_name = form.cleaned_data.get('mat_name')
            description = form.cleaned_data.get('description')
            link = form.cleaned_data.get('link')
            date_added = form.cleaned_data.get('date_added')

            if category == 'material':
                cat='CM'
            elif category == 'pq':
                cat='PQ'
            elif category == 'solution':
                cat='SS'

            # Generate Unique ReceiptNo
            #############################
            # Randomly Choose Letters for adding to code
            def gencode(cat):
                char1 = random.choice(string.ascii_uppercase)
                char2 = random.choice(string.ascii_lowercase)
                char3 = random.choice(string.ascii_letters)
                char4 = random.choice('1234567890')

                year = timezone.now().year

                return f"RSRC/{cat}/{year}/{char1}{char2}{char4}{char3}"

            rsd = gencode(cat)
            resource_code = rsd
            while Resource.objects.filter(resource_code=rsd):
                rsd = gencode()
                if not Resource.objects.filter(resource_code=gencode):
                    resource_code = gencode

            rs = Resource.objects.create(
                course=course,
                category=category,
                mat_name=mat_name,
                description=description,
                resource_code=resource_code,
                date_added=date_added,
                link=link,
            )
            rs.save()

            # Redirect to dashboard
            messages.success(request, 'Resource Uploaded Successfully')
            return HttpResponseRedirect(reverse("administrator:upload"))
        else:
            messages.error(request, 'Something Went Wrong')
            return HttpResponseRedirect(reverse("administrator:upload"))

    
    context = {
        'form': form,
        'courses': courses,
        'categories': categories,
    }

    return render(request, 'administrator/dashboard/upload.html', context)


@login_required()
def newCourse(request):
    # Get the course list
    courses = Course.objects.all()

    # Get Categories List
    categories = {
    'material': 'Course Material',
    'pq': 'Past Question',
    'solution': 'Suggested Solution',
    'ican': 'ICAN'
    }

    # Create view function to upload resources
    form = CourseCreationForm(request.POST or None)

    # Check for form submission
    if request.method == "POST":
        # Check form submission
        if form.is_valid():
            # Get the form fields
            course_title = form.cleaned_data.get('course_title')
            course_code = form.cleaned_data.get('course_code')
            level = form.cleaned_data.get('level')

            crs = Course.objects.create(
                course_title=course_title,
                course_code=course_code,
                level=level,
            )
            crs.save()

            # Redirect to dashboard
            messages.success(request, 'Course Added Successfully')
            return HttpResponseRedirect(reverse("administrator:newCourse"))
        else:
            messages.error(request, 'Something Went Wrong')
            return HttpResponseRedirect(reverse("administrator:newCourse"))

    
    context = {
        'form': form,
        'courses': courses,
        'categories': categories,
    }

    return render(request, 'administrator/dashboard/newCourse.html', context)


# Create the edu_search view using a listview class
class edu_search(ListView):
    model = Resource
    template_name = 'administrator/dashboard/edu_search.html'
    context_object_name = 'resources'
    paginate_by = 6

    # Get the course list
    courses = Course.objects.all()

    # Get Categories List
    categories = {
    'material': 'Course Material',
    'pq': 'Past Question',
    'solution': 'Suggested Solution',
    'ican': 'ICAN'
    }

    extra_context = {
        'courses': courses,
        'categories': categories,
    }

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(edu_search, self).get_context_data(**kwargs)
        query1 = self.request.GET.get('q1')
        query2 = self.request.GET.get('q2')

        if query1 is None and query2 is None:
            allresources = Resource.objects.all()
            context['searchq'] = allresources
        else:
            context['searchq1'] = query1
            context['searchq2'] = query2
        return context

    def get_queryset(self):
        queryset = super(edu_search, self).get_queryset()
        query1 = self.request.GET.get('q1')
        query2 = self.request.GET.get('q2')

        if query1 is None and query2 is None:
            return queryset
        else:
            if query1 != 'none' and query2 != 'none':
                # Get the resources for the course under the searched category
                try:
                    course_id = Course.objects.get(course_code=query1)
                    queryset = Resource.objects.filter(course=course_id, category=query2)
                except ObjectDoesNotExist:
                    queryset = None
            elif query1 != 'none' and query2 == 'none':
                try:
                    course_id = Course.objects.get(course_code=query1)
                    queryset = Resource.objects.filter(course=course_id)
                except ObjectDoesNotExist:
                    queryset = None
            elif query1 == 'none' and query2 != 'none':
                try:
                    queryset = Resource.objects.filter(category=query2)
                except ObjectDoesNotExist:
                    queryset = None

            return queryset


# Create a view function that takes request, level, category and show returns a resources from the resource model that are for courses for that level and of the category inserted in the function
@login_required()
def resource_library(request, category, level):
    if category is None:
        messages.error(request, 'No Category Selected')
        return HttpResponseRedirect(reverse("administrator:edu_dashboard"))
    else:
        if level is None:
            messages.error(request, 'No Level Selected')
            return HttpResponseRedirect(reverse("administrator:edu_dashboard"))
        else:
            try:
                # Retrieve courses for the specified level
                courses_for_level = Course.objects.filter(level=level)
            except ObjectDoesNotExist:
                messages.error(request, 'Something Went Wrong')
                return HttpResponseRedirect(reverse("administrator:edu_dashboard"))
    
    # Retrieve resources for the specified level and category
    resources = Resource.objects.filter(course__in=courses_for_level, category=category)

    # Get the course list
    courses = Course.objects.all()

    # Get Categories List
    categories = {
    'material': 'Course Material',
    'pq': 'Past Question',
    'solution': 'Suggested Solution',
    'ican': 'ICAN'
    }

     
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(resources, 6)  # Show 6 resources per page

    try:
        resources = paginator.page(page)
    except PageNotAnInteger:
        resources = paginator.page(1)
    except EmptyPage:
        resources = paginator.page(paginator.num_pages)
    
    total = len(resources)

    context = {
        'resources': resources,
        'category': category,
        'level': level,
        'courses': courses,
        'categories': categories,
        'count': total,
    }
    
    return render(request, 'administrator/dashboard/resource_library.html', context)

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
    
# Create a function that exports students table as an excel file