from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from wttapp.models import Workday
from UserLogin.models import UserProfile
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import WorkdayForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime,timedelta, time
from django.http import JsonResponse
from django.views import View
from django.db.models import Q, Sum, Count, F, ExpressionWrapper, fields
from django.db.models.functions import ExtractYear



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
        records_list = Workday.objects.select_related('user__user_profile').all().order_by('-date')  # Show all records
    else:
        records_list = Workday.objects.select_related('user__user_profile').filter(user=request.user).order_by('-date')  # Show only the user's records

    # Pagination logic
    paginator = Paginator(records_list, 5)  # Show 5 records per page
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
            return redirect('home')  
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
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Get the current date, month, and year
    current_date = datetime.now()
    current_month = datetime.now().strftime('%B')
    current_year = datetime.now().year
    
    # Calculate the previous month and year
    previous_date = current_date - timedelta(days=current_date.day)
    previous_month = previous_date.strftime('%B') 
    previous_year = previous_date.year
    
    # Default to the current month if no month is selected
    selected_month = request.GET.get('month', current_month)
    
    # Filter by workday type
    selected_type = request.GET.get('workday_type')
    
    # Filter by year (default to current year)
    selected_year = request.GET.get('year', current_year)
    
    # Handle empty selected_year (convert to current year)
    if selected_year == '':
        selected_year = current_year
    
    # Filter by user (only for Managers and System Admins)
    selected_user = request.GET.get('user')
    
    # Handle empty selected_user (convert to None)
    if selected_user == '':
        selected_user = None
    
    # Get the selected user's username (if a user is selected)
    selected_user_username = None
    if selected_user:
        selected_user_username = User.objects.get(id=selected_user).username
    
    # Check if the user is a Manager or System Admin
    if user_profile.position in ['Manager', 'System Admin']:
        # Show all data for Managers and System Admins
        workdays = Workday.objects.all().order_by('-date')
        
        # Apply user filter if selected
        if selected_user:
            workdays = workdays.filter(user_id=selected_user)
    else:
        # Show only the user's data for Staff
        workdays = Workday.objects.filter(user=request.user).order_by('-date')
    
    # Apply month filter
    if selected_month:
        workdays = workdays.filter(month=selected_month)
    
    # Apply workday type filter
    if selected_type:
        workdays = workdays.filter(workday_type=selected_type)
    
    # Apply year filter (default to current year)
    workdays = workdays.filter(date__year=selected_year)
    
    # Exclude records where time_in or time_out is None
    workdays = workdays.exclude(time_in__isnull=True).exclude(time_out__isnull=True)
    
    # Calculate totals for the selected filters
    total_entries = workdays.count()
    
    # Calculate total hours dynamically
    total_hours = timedelta()
    for workday in workdays:
        # Combine date with time_in and time_out to create datetime objects
        datetime_in = datetime.combine(workday.date, workday.time_in)
        datetime_out = datetime.combine(workday.date, workday.time_out)
        
        # Calculate duration
        duration = datetime_out - datetime_in
        total_hours += duration
    
    # Convert total_hours to hours
    total_hours = total_hours.total_seconds() / 3600  # Convert timedelta to hours
    
    # Calculate workday type counts
    workday_type_counts = {
        'Work': workdays.filter(workday_type='Work').count(),
        'Sick_Leave': workdays.filter(workday_type='Sick Leave').count(),
        'Annual_Leave': workdays.filter(workday_type='Annual Leave').count(),
        'Bank_Holiday': workdays.filter(workday_type='Bank Holiday').count(),
    }
    
    # Calculate total Annual Leave hours for the current year
    annual_leave_hours = timedelta()
    if user_profile.position in ['Manager', 'System Admin']:
        # For Managers and System Admins, calculate Annual Leave for all users (or selected user)
        if selected_user:
            annual_workdays = workdays.filter(workday_type='Annual Leave')
        else:
            annual_workdays = Workday.objects.filter(
                workday_type='Annual Leave',
                date__year=current_year
            ).exclude(time_in__isnull=True).exclude(time_out__isnull=True)
    else:
        # For Staff, calculate Annual Leave for the logged-in user
        annual_workdays = workdays.filter(
            workday_type='Annual Leave',
            user=request.user
        )
    
    for workday in annual_workdays:
        # Combine date with time_in and time_out to create datetime objects
        datetime_in = datetime.combine(workday.date, workday.time_in)
        datetime_out = datetime.combine(workday.date, workday.time_out)
        
        # Calculate duration
        duration = datetime_out - datetime_in
        annual_leave_hours += duration
    
    # Convert annual_leave_hours to hours
    annual_leave_hours = annual_leave_hours.total_seconds() / 3600  # Convert timedelta to hours
    
    # Calculate monthly hours for the current year
    monthly_hours = {month: 0 for month in [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]}
    for workday in workdays:
        month = workday.date.strftime('%B')
        datetime_in = datetime.combine(workday.date, workday.time_in)
        datetime_out = datetime.combine(workday.date, workday.time_out)
        duration = (datetime_out - datetime_in).total_seconds() / 3600  # Convert timedelta to hours
        monthly_hours[month] += duration
    
    # Get unique years for the year filter dropdown
    years = Workday.objects.dates('date', 'year').values_list('date__year', flat=True).distinct()
    
    # User filter (only for Managers and System Admins)
    users = User.objects.all() if user_profile.position in ['Manager', 'System Admin'] else None
    
    # Pass the filtered workdays and filter options to the template
    context = {
        'workdays': workdays,
        'months': Workday.MONTH_CHOICES,
        'workday_types': Workday.WORKDAY_TYPE_CHOICES,
        'years': years,
        'selected_month': selected_month,
        'selected_type': selected_type,
        'selected_year': selected_year,
        'total_entries': total_entries,
        'total_hours': total_hours,
        'workday_type_counts': workday_type_counts,
        'monthly_hours': monthly_hours,
        'current_month': current_month,
        'previous_month': previous_month,
        'current_year': current_year,
        'previous_year': previous_year,
        'user_profile': user_profile,
        'users': users,  # Pass users for the filter dropdown
        'selected_user': int(selected_user) if selected_user else None,
        'selected_user_username': selected_user_username,  # Pass the selected user's username
        'annual_leave_hours': annual_leave_hours,  # Pass Annual Leave hours to the template
    }
    return render(request, 'wttapp/dashboard.html', context)