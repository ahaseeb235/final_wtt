''' urls.py for wttapp '''

from django.urls import path
from . import views
from wttapp.views import export_workdays_csv




urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_record, name='create_record'),
    path('edit/<int:pk>/', views.edit_workday, name='edit_workday'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('export-workdays-csv/', export_workdays_csv, name='export_workdays_csv'),
    
]