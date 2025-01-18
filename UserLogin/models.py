from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    
    # Fields synced with the User model
    username = models.CharField(max_length=150, editable=False)  # Automatically populated
    firstname = models.CharField(max_length=30, null=False, editable=True)  # Automatically populated
    lastname = models.CharField(max_length=150, null=False, editable=True)  # Automatically populated
    email = models.EmailField(null=True, editable=True)  # Automatically populated
    
    # Additional fields
    emergency_contact = models.CharField(max_length=100, blank=True, null=True, help_text="Emergency contact name and number.")
    manager_name = models.ForeignKey(
        User, 
        related_name='user_manager', 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
    )
    
    # Position field with help text
    POSITION_CHOICES = [
        ('Staff', 'Staff'),
        ('Manager', 'Manager'),
        ('System Admin', 'System Admin'),
    ]
    position = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        default='Staff',
        help_text="This can be edited by your manager or System admin."
    )
    
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Former', 'Former'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Active',
        help_text="User status (Active or Former)."
    )
    
    # Profile picture
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.position}"
    
    def save(self, *args, **kwargs):
        """Override save method to sync fields with the User model."""
        if not self.username:
            self.username = self.user.username
        if not self.firstname:
            self.firstname = self.user.first_name
        if not self.lastname:
            self.lastname = self.user.last_name
        if not self.email:
            self.email = self.user.email
        super().save(*args, **kwargs)
    
    # To access Workday instances from UserProfile
    def get_workdays(self):
        """Returns all Workday instances associated with this user."""
        return self.user.user_workdays.all()

# Signals to create and save UserProfile
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save the UserProfile whenever the User is saved.
    """
    if hasattr(instance, 'user_profile'):
        instance.user_profile.save()
    else:
        # Create a UserProfile if it doesn't exist
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save the UserProfile whenever the User is saved.
    """
    instance.user_profile.save()