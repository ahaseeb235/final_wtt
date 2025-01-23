from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from wttapp.models import Workday
from UserLogin.models import UserProfile
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import WorkdayForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
import json



class WorkdayListView(LoginRequiredMixin, ListView):
    model = Workday
    template_name = 'wttapp/home.html'
    context_object_name = 'records'
    paginate_by = 5  # Add pagination directly in the ListView

    def get_queryset(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        
        # Check if the user is an active System Admin or Manager
        if user_profile.status == 'Active' and user_profile.position in ['System Admin', 'Manager']:
            return Workday.objects.all()  # Show all records
        else:
            return Workday.objects.filter(user=self.request.user)  # Show only the user's records

@login_required
def home(request):
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Check if the user is an active System Admin or Manager
    if user_profile.status == 'Active' and user_profile.position in ['System Admin', 'Manager']:
        records_list = Workday.objects.select_related('user__user_profile').all()  # Show all records
    else:
        records_list = Workday.objects.select_related('user__user_profile').filter(user=request.user)  # Show only the user's records

    # Pagination logic
    paginator = Paginator(records_list, 5)  # Show 3 records per page
    page = request.GET.get('page', 1)  # Get the current page number from the request

    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        records = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        records = paginator.page(paginator.num_pages)

    return render(request, 'wttapp/home.html', {'records': records, 'user_profile': user_profile})

@login_required
def create_record(request):
    if request.method == 'POST':
        form = WorkdayForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the home page or another view
    else:
        form = WorkdayForm(user=request.user)
    
    return render(request, 'wttapp/create_record.html', {'form': form})

@login_required
def edit_workday(request, pk):
    workday = get_object_or_404(Workday, id=pk)

    # Ensure the user is the owner of the record or an admin/manager
    if workday.user != request.user and not request.user.user_profile.position in ['System Admin', 'Manager']:
        return redirect('home')  # Redirect unauthorized users

    if request.method == 'POST':
        form = WorkdayForm(request.POST, instance=workday, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = WorkdayForm(instance=workday, user=request.user)
    
    return render(request, 'wttapp/edit_workday.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    user_profile = user.user_profile
    
    # Get the selected month from the request (default to current month)
    selected_month = request.GET.get('month', datetime.now().strftime('%B'))
    
    # Filter Workday data based on user position
    if user_profile.position in ['System Admin', 'Manager']:
        workdays = Workday.objects.filter(month=selected_month)
    else:
        workdays = Workday.objects.filter(user=user, month=selected_month)
    
    # Prepare data for the chart
    chart_labels = []
    chart_data = []
    
    for workday in workdays:
        chart_labels.append(workday.user.get_full_name())
        chart_data.append(float(workday.total_hours))
    
    # Convert data to JSON for JavaScript
    chart_labels_json = json.dumps(chart_labels)
    chart_data_json = json.dumps(chart_data)
    
    # Prepare data for the template
    context = {
        'workdays': workdays,
        'selected_month': selected_month,
        'user_profile': user_profile,
        'chart_labels_json': chart_labels_json,
        'chart_data_json': chart_data_json,
        'month_choices': Workday.MONTH_CHOICES, 
    }
    
    return render(request, 'wttapp/dashboard.html', context)