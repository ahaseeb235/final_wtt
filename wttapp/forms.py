from django.contrib.auth.models import User
from .models import Workday
from UserLogin.models import UserProfile
from django import forms

# forms.py for wttapp app


class WorkdayForm(forms.ModelForm):
    class Meta:
        model = Workday
        fields = ['name', 'date', 'month', 'workday_type', 'time_in', 'time_out']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time_in': forms.TimeInput(attrs={'type': 'time'}),
            'time_out': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get the user from kwargs
        super().__init__(*args, **kwargs)

        # Auto-populate the name field based on the UserProfile
        if self.user:
            user_profile = UserProfile.objects.get(user=self.user)
            self.fields['name'] = forms.CharField(
                initial=f"{user_profile.firstname} {user_profile.lastname}",
                disabled=True,  # Make the field read-only
                required=False,  # Not required since it's auto-populated
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user  # Assign the user to the Workday instance
        if commit:
            instance.save()
        return instance