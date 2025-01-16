# tests.py for wttapp app

from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Workday
from django.urls import reverse
from datetime import  date, time

class WorkdayModelTest(TestCase):

    def setUp(self):
        # Create a User instance
        self.user = User.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            password='testpassword123'
        )

        # Create a Workday instance
        self.workday = Workday.objects.create(
            user=self.user,
            date=date.today(),
            month='January',
            workday_type='Work',
            time_in=time(9, 0),
            time_out=time(17, 0),
        )

    def test_workday_creation(self):
        """To test that a Workday instance is created correctly."""
        self.assertEqual(self.workday.user.username, 'testuser')
        self.assertEqual(self.workday.date, date.today())
        self.assertEqual(self.workday.month, 'January')
        self.assertEqual(self.workday.workday_type, 'Work')
        self.assertEqual(self.workday.time_in, time(9, 0))
        self.assertEqual(self.workday.time_out, time(17, 0))
        self.assertEqual(self.workday.name, 'Test User')

    def test_workday_str_method(self):
        """Test the __str__ method of the Workday model."""
        expected_str = f"Test User - {date.today()} (Work)"
        self.assertEqual(str(self.workday), expected_str)

    def test_workday_total_hours_property(self):
        """Test the total_hours property for a Workday."""
        self.assertEqual(self.workday.total_hours, 8.0)  # 9 AM to 5 PM is 8 hours

        # Test with no time_in or time_out
        self.workday.time_in = None
        self.workday.time_out = None
        self.assertEqual(self.workday.total_hours, 0)

    def test_workday_clean_method(self):
        """Test the clean method for validation of time_in and time_out."""
        # Test for Workday type 'Work' with missing time_in or time_out
        self.workday.time_in = None
        with self.assertRaises(ValidationError):
            self.workday.clean()

        self.workday.time_in = time(9, 0)
        self.workday.time_out = None
        with self.assertRaises(ValidationError):
            self.workday.clean()

        # Test for Workday type 'Sick Leave' with time_in or time_out
        self.workday.workday_type = 'Sick Leave'
        self.workday.time_in = time(9, 0)
        self.workday.time_out = time(17, 0)
        with self.assertRaises(ValidationError):
            self.workday.clean()

        # Test for Workday type 'Annual Leave' with time_in or time_out
        self.workday.workday_type = 'Annual Leave'
        with self.assertRaises(ValidationError):
            self.workday.clean()

        # Test for Workday type 'Bank Holiday' with time_in or time_out
        self.workday.workday_type = 'Bank Holiday'
        with self.assertRaises(ValidationError):
            self.workday.clean()

    def test_workday_save_method(self):
        """Test the save method to ensure name is populated and clean is called."""
        # Ensure the name field is populated
        self.assertEqual(self.workday.name, 'Test User')

        # Test that clean is called during save
        self.workday.workday_type = 'Sick Leave'
        self.workday.time_in = time(9, 0)
        self.workday.time_out = time(17, 0)
        with self.assertRaises(ValidationError):
            self.workday.save()

    def test_workday_month_choices(self):
        """Test that the month field only accepts valid choices."""
        valid_months = ['January', 'February', 'March', 'April', 'May', 'June',
                        'July', 'August', 'September', 'October', 'November', 'December']
        for month in valid_months:
            self.workday.month = month
            self.workday.save()
            self.assertEqual(self.workday.month, month)

        with self.assertRaises(ValidationError):
            self.workday.month = 'InvalidMonth'
            self.workday.full_clean()

    def test_workday_type_choices(self):
        """Test that the workday_type field only accepts valid choices."""
        valid_types = ['Work', 'Sick Leave', 'Annual Leave', 'Bank Holiday']
        for workday_type in valid_types:
            self.workday.workday_type = workday_type
            self.workday.save()
            self.assertEqual(self.workday.workday_type, workday_type)

        with self.assertRaises(ValidationError):
            self.workday.workday_type = 'InvalidType'
            self.workday.full_clean()

    def tearDown(self):
        # Clean up after tests
        self.user.delete()
        self.workday.delete()