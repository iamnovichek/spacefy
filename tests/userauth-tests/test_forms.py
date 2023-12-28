from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.userauth.models import CustomUser, UserProfile
from apps.userauth.forms import SignupForm


class TestCustomSignupForm(TestCase):
    def setUp(self) -> None:
        self.form = SignupForm(data={
            "username": "tester",
            "first_name": "John",
            "last_name": "Doe",
            "email": "test@gmail.com",
            "password1": "<PASSWORD>",
            "password2": "<PASSWORD>"
        })

    def test_clean_valid_data(self):
        self.assertTrue(self.form.is_valid())

    def test_clean_invalid_username(self):
        self.form.data['username'] = 'a'
        self.assertFalse(self.form.is_valid())
        with self.assertRaises(ValidationError):
            self.form.clean()

    def test_clean_invalid_first_name(self):
        self.form.data['first_name'] = 'J'
        self.assertFalse(self.form.is_valid())
        with self.assertRaises(ValidationError):
            self.form.clean()

    def test_clean_invalid_last_name(self):
        self.form.data['last_name'] = 'D'
        self.assertFalse(self.form.is_valid())
        with self.assertRaises(ValidationError):
            self.form.clean()

    def test_clean_password_dont_match(self):
        self.form.data['password1'] = 'PASSWORD'
        self.assertFalse(self.form.is_valid())
        with self.assertRaises(ValidationError):
            self.form.clean()

    def test_clean_userprofile_exists(self):
        self.form.is_valid()
        self.form.save()

        self.assertTrue(self.form.is_valid())
        with self.assertRaises(ValidationError):
            self.form.clean()

    def test_save(self):
        self.assertTrue(self.form.is_valid())
        new_user = self.form.save()

        self.assertEqual(new_user.email, 'test@gmail.com')
        self.assertTrue(CustomUser.objects.filter(email=new_user.email).exists())
        self.assertTrue(UserProfile.objects.filter(username="tester").exists())

        new_profile = UserProfile.objects.get(user=new_user)

        self.assertEqual(new_profile.username, 'tester')
        self.assertEqual(new_profile.first_name, 'John')
        self.assertEqual(new_profile.last_name, 'Doe')
