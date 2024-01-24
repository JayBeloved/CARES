
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
            path('finance/search/matric', views.search, name='search'),
            path('academic/dashboard/', views.edu_dashboard, name='edu_dashboard'),
            path('academic/dashboard/resources', views.ResourcesListView.as_view(), name='resources'),
        ], 'cares'), namespace='administrator')),

    path('academic/', include(([
            
            # path('upload/resource/', views.verify, name='verify'),
            # path('search/matric', views.search, name='search'),
        ], 'cares'), namespace='academic'))
]