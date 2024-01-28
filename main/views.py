import pandas as pd
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView
from .models import Student, Resource, Course
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def home(request):
    return render(request, 'main/home.html')

def contribute(request):
    return render(request, 'main/contribute.html')

def hub(request):
    # Check if there are resources in the database
    all_resources, course_materials, past_questions, ican, solution = (0,0,0,0,0)
    courses = []
    recent_resources = []
    categories = []
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

        # Get the recently added materials
        recent_resources = Resource.objects.all().order_by('-date_added')[:6]

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
        'resources': recent_resources,
        'courses': courses,
        'categories': categories,
    }


    return render(request, 'main/resources.html', context)

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


class hub_search(ListView):
    model = Resource
    template_name = 'main/hub_search.html'
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
        context = super(hub_search, self).get_context_data(**kwargs)
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
        queryset = super(hub_search, self).get_queryset()
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
    
    return render(request, 'main/resource_library.html', context)


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