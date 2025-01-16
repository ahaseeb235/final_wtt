''' urls.py for wttapp '''

from django.urls import path
from . import views

app_name = 'wttapp'

urlpatterns = [
    path('', views.home, name='home'),
    
]