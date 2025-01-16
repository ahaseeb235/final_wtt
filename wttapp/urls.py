''' urls.py for wttapp '''

from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_record, name='create_record'),
    
]