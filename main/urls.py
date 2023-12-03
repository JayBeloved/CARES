from django.urls import path, include
from . import views

urlpatterns = [
    path('', include(([
        path('', views.home, name='home'),
        path('contribute', views.contribute, name="contribute"),
        path('access', views.access, name="access"),
        path('about', views.about, name="about"),
        path('verify', views.verify, name="verify"),
        path('receipt/<int:student_id>', views.receipt, name="receipt"),
        # path('import', views.import_excel, name="import"),
    ], 'ereceipt'), namespace='main')),
]