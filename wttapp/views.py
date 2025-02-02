from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from wttapp.models import Workday
from UserLogin.models import UserProfile
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import WorkdayForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime,timedelta
from django.http import JsonResponse
from django.views import View
from django.db.models import Q, Sum, Count
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
        records_list = Workday.objects.select_related('user__user_profile').all()  # Show all records
    else:
        records_list = Workday.objects.select_related('user__user_profile').filter(user=request.user)  # Show only the user's records

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
    # Get the current month as a string (e.g., 'January', 'February', etc.)
    current_month = datetime.now().strftime('%B')

    # Default to the current month if no month is selected
    selected_month = request.GET.get('month', current_month)

    # Get all workday entries for the logged-in user, ordered by created_date descending
    workdays = Workday.objects.filter(user=request.user).order_by('-date')

    # Apply month filter
    if selected_month:
        workdays = workdays.filter(month=selected_month)

    # Filter by workday type
    selected_type = request.GET.get('workday_type')
    if selected_type:
        workdays = workdays.filter(workday_type=selected_type)

    # Filter by year (extracted from the date field)
    selected_year = request.GET.get('year')
    if selected_year:
        workdays = workdays.filter(date__year=selected_year)

    # Get unique years for the year filter dropdown
    years = Workday.objects.filter(user=request.user).annotate(
        yearView=ExtractYear('date')
    ).values_list('yearView', flat=True).distinct()
    
    # Calculate totals for the selected filters
    total_entries = workdays.count()
    total_hours = sum(record.total_hours for record in workdays)

    # Calculate workday type counts
    workday_type_counts = {
        'Work': workdays.filter(workday_type='Work').count(),
        'Sick_Leave': workdays.filter(workday_type='Sick Leave').count(),
        'Annual_Leave': workdays.filter(workday_type='Annual Leave').count(),
        'Bank_Holiday': workdays.filter(workday_type='Bank Holiday').count(),
    }

    # Calculate monthly hours
    monthly_hours = {month: 0 for month in [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]}
    for workday in workdays:
        month = workday.date.strftime('%B')
        monthly_hours[month] += workday.total_hours or 0

    # Get unique years and months for filters
    years = Workday.objects.dates('date', 'year').values_list('date__year', flat=True).distinct()
    months = Workday.MONTH_CHOICES

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
    }
    return render(request, 'wttapp/dashboard.html', context)