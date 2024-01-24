
from django.urls import path, include
from django.contrib.auth.views import LogoutView as logout_view
from . import views

urlpatterns = [
    path('administrator/', include(([
            path('', views.login_redirect, name="landing"),
            path('login/', views.login_view, name="login"),
            path('logout/', logout_view.as_view(), name="logout"),
            path('dashboard/', views.dashboard, name='dashboard'),
            path('dashboard/students', views.StudentsListView.as_view(), name='students'),
            path('verify/student/<int:student_id>', views.verify, name='verify'),
            path('search/matric', views.search, name='search'),
        ], 'cares'), namespace='administrator'))

    path('academic/', include(([
            path('', views.login_redirect, name="landing"),
            path('login/', views.login_view, name="login"),
            path('logout/', logout_view.as_view(), name="logout"),
            path('dashboard/', views.dashboard, name='edu_dashboard'),
            path('dashboard/resources', views.ResourcesListView.as_view(), name='resources'),
            # path('upload/resource/', views.verify, name='verify'),
            # path('search/matric', views.search, name='search'),
        ], 'cares'), namespace='academic'))
]