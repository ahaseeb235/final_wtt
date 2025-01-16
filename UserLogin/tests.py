# tests.py for Userlogin app

from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile
from django.core.files.uploadedfile import SimpleUploadedFile

class UserProfileModelTest(TestCase):

    def setUp(self):
        # Create a User instance
        self.user = User.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            password='testpassword123'
        )
        
        # Create a UserProfile instance
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            emergency_contact='Emergency Contact Info',
            position='Staff',
            profile_picture=SimpleUploadedFile(
                name='test_image.jpg',
                content=open('path_to_test_image.jpg', 'rb').read(),
                content_type='image/jpeg'
            )
        )

    def test_user_profile_creation(self):
        """Test that a UserProfile instance is created correctly."""
        self.assertEqual(self.user_profile.user.username, 'testuser')
        self.assertEqual(self.user_profile.firstname, 'Test')
        self.assertEqual(self.user_profile.lastname, 'User')
        self.assertEqual(self.user_profile.email, 'testuser@example.com')
        self.assertEqual(self.user_profile.emergency_contact, 'Emergency Contact Info')
        self.assertEqual(self.user_profile.position, 'Staff')
        self.assertTrue(self.user_profile.profile_picture)

    def test_user_profile_save_method(self):
        """Test the save method to ensure fields are synced with the User model."""
        self.user.first_name = 'UpdatedFirst'
        self.user.last_name = 'UpdatedLast'
        self.user.email = 'updated@example.com'
        self.user.save()

        self.user_profile.save()  # Trigger the save method

        self.assertEqual(self.user_profile.firstname, 'UpdatedFirst')
        self.assertEqual(self.user_profile.lastname, 'UpdatedLast')
        self.assertEqual(self.user_profile.email, 'updated@example.com')

    def test_user_profile_str_method(self):
        """Test the __str__ method of the UserProfile model."""
        self.assertEqual(str(self.user_profile), 'testuser - Staff')

    def test_user_profile_get_workdays_method(self):
        """Test the get_workdays method of the UserProfile model."""
        # Assuming you have a Workday model related to UserProfile
        # You can add Workday instances here and test the method
        workdays = self.user_profile.get_workdays()
        self.assertEqual(workdays.count(), 0)  # Initially, no workdays

    def test_user_profile_position_choices(self):
        """Test that the position field only accepts valid choices."""
        valid_positions = ['Staff', 'Manager', 'System Admin']
        for position in valid_positions:
            self.user_profile.position = position
            self.user_profile.save()
            self.assertEqual(self.user_profile.position, position)

        with self.assertRaises(ValueError):
            self.user_profile.position = 'InvalidPosition'
            self.user_profile.save()

    def test_user_profile_manager_name(self):
        """Test the manager_name ForeignKey relationship."""
        manager_user = User.objects.create_user(
            username='manageruser',
            first_name='Manager',
            last_name='User',
            email='manager@example.com',
            password='managerpassword123'
        )
        self.user_profile.manager_name = manager_user
        self.user_profile.save()

        self.assertEqual(self.user_profile.manager_name.username, 'manageruser')

    def tearDown(self):
        # Clean up after tests
        self.user.delete()
        self.user_profile.delete()