from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import UserProfile
from django import forms
from django.forms.widgets import PasswordInput, TextInput

# register / create user form

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
# login form

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'validate', 'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'})) 
    
# user profile form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['firstname', 'lastname', 'email', 'status', 'emergency_contact', 'profile_picture', 'position', 'manager_name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get the current user from kwargs
        super(UserProfileForm, self).__init__(*args, **kwargs)

    # Make 'position' and 'manager_name' fields read-only
        self.fields['position'].disabled = True
        self.fields['manager_name'].disabled = True
        
    def clean_profile_picture(self):
        """To handle the profile picture field."""
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture is None:  # If the user clears the image field
            return 'profile_pictures/default.png'  # Revert to the default image
        return profile_picture
            
# user change form
class UserProfileChange(UserChangeForm):
    class Meta:
        model = UserProfile
        fields = ['firstname', 'lastname', 'email', 'emergency_contact', 'profile_picture']
        
# Password Change Form
class PasswordChangeCustomForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
        
# manager or system admin updates user
class UserEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['firstname', 'lastname', 'email', 'status', 'emergency_contact', 'position', 'manager_name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get the current user from kwargs
        super(UserEditForm, self).__init__(*args, **kwargs)

        # Make all fields read-only except for 'status' and 'manager_name'
        for field_name, field in self.fields.items():
            if field_name not in ['position', 'status', 'manager_name']:
                field.widget.attrs['readonly'] = True  
                field.required = False  # Make the field not required