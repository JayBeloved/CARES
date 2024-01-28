from django.urls import path, include
from . import views

urlpatterns = [
    path('', include(([
        path('', views.home, name='home'),
        path('contribute', views.contribute, name="contribute"),
        path('resources/dashboard', views.hub, name="access"),
        path('about', views.about, name="about"),
        path('verify', views.verify, name="verify"),
        path('receipt/<int:student_id>', views.receipt, name="receipt"),
        path('resources/search/', views.hub_search.as_view(), name='hub_search'),
        path('academic/resources/<str:category>/<str:level>/', views.resource_library, name='resource_library'),
        # path('import', views.import_excel, name="import"),
    ], 'ereceipt'), namespace='main')),
]