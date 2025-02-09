from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import UserCreationForm, UserProfileForm, PasswordChangeCustomForm, UserEditForm
from .models import UserProfile

# User Registration View
def register(request):
    form = UserCreationForm()
    registered = False
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            registered = True
            messages.success(request, 'Registration successful! And you are in.')
            return redirect('login')
    return render(request, 'UserLogin/register.html', {'form': form})

# User Login View
def userlogin(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
    return render(request, 'UserLogin/login.html', {'form': form})

# User Logout View
@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

# User Profile View
@login_required
def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Create a UserProfile if it doesn't exist
        user_profile = UserProfile.objects.create(user=request.user)
    return render(request, 'UserLogin/profile.html', {'user_profile': user_profile})

# Edit Profile View
@login_required
def edit_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    profile_form = UserProfileForm(instance=user_profile, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile, user=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
       

    return render(request, 'UserLogin/edit_profile.html', {
        'profile_form': profile_form,
        'user_profile': user_profile,
    })

# Change Password View
@login_required
def change_password(request):
    if request.method == 'POST':
        password_form = PasswordChangeCustomForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        password_form = PasswordChangeCustomForm(request.user)

    return render(request, 'UserLogin/change_password.html', {
        'password_form': password_form,
    })
    
    

@login_required
def remove_profile_picture(request):
    """Allows users to reset their profile picture to default."""
    user_profile = request.user.user_profile
    user_profile.remove_profile_picture()
    return redirect('profile')
    




# Check if the user is a System Admin or Manager
def is_admin_or_manager(user):
    return user.user_profile.position in ['System Admin', 'Manager']

# List all users
@login_required
@user_passes_test(is_admin_or_manager)
def user_list(request):
    users = UserProfile.objects.all()
    return render(request, 'UserLogin/user_list.html', {'users': users})

# Edit user fields (position and manager)
@login_required
@user_passes_test(is_admin_or_manager)
def edit_user(request, user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User profile updated successfully!')
            return redirect('user_list')  # Redirect to the user list page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserEditForm(instance=user_profile, user=request.user)
    return render(request, 'UserLogin/edit_user.html', {'form': form, 'user_profile': user_profile})