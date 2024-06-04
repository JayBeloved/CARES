
from django.urls import path, include
from django.contrib.auth.views import LogoutView as logout_view
from . import views

urlpatterns = [
    path('administrator/', include(([
            path('', views.login_redirect, name="landing"),
            path('login/', views.login_view, name="login"),
            path('logout/', logout_view.as_view(), name="logout"),
            path('finance/dashboard/', views.dashboard, name='dashboard'),
            path('finance/dashboard/students', views.StudentsListView.as_view(), name='students'),
            path('finance/verify/student/<int:student_id>', views.verify, name='verify'),
            path('finance/verify/multiple/', views.verify_multiple, name='verify_multiple'),
            path('finance/search/matric', views.search, name='search'),
            path('academic/dashboard/', views.edu_dashboard, name='edu_dashboard'),
            path('academic/dashboard/resources', views.ResourcesListView.as_view(), name='resources'),
            path('academic/dashboard/resources/upload', views.upload_resource, name='upload'),
            path('academic/dashboard/courses/new', views.newCourse, name='newCourse'),
            path('academic/search/resources/', views.edu_search.as_view(), name='edu_search'),
            path('academic/resources/<str:category>/<str:level>/', views.resource_library, name='resource_library'),
            path('export_excel/', views.export_excel, name='export_excel'),
        ], 'cares'), namespace='administrator')),
]