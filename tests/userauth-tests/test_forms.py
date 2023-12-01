from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.userauth.models import CustomUser, UserProfile
from apps.userauth.forms import CustomSignupForm


class TestCustomSignupForm(TestCase):
    def setUp(self) -> None:
        self.valid_form = CustomSignupForm(
            data={
                "username": "user",
                "first_name": "John",
                "last_name": "Doe",
                "password1": "password123",
                "password2": "password123"
            }
        )

        self.invalid_username_form = CustomSignupForm(
            data={
                "username": "u",
                "first_name": "John",
                "last_name": "Doe",
                "password1": "password123",
                "password2": "password123"
            }
        )

        self.invalid_first_name_form = CustomSignupForm(
            data={
                "username": "user",
                "first_name": "J",
                "last_name": "Doe",
                "password1": "password123",
                "password2": "password123"
            }
        )

        self.invalid_last_name_form = CustomSignupForm(
            data={
                "username": "user",
                "first_name": "John",
                "last_name": "D",
                "password1": "password123",
                "password2": "password123"
            }
        )

        self.password_dont_match_form = CustomSignupForm(
            data={
                "username": "user",
                "first_name": "John",
                "last_name": "Doe",
                "password1": "password123",
                "password2": "password"
            }
        )

        user = CustomUser.objects.create_user(
            email="test@gmail.com",
            password="password123"
        )

        self.userprofile = UserProfile(
            user=user,
            username="user",
            first_name="John",
            last_name="Doe",
        )

        self.user_already_exists_form = CustomSignupForm(
            data={
                "username": "user",
                "first_name": "John",
                "last_name": "Doe",
                "password1": "password123",
                "password2": "password123"
            }
        )

    def test_clean_valid_data(self) -> None:
        cleaned_data = self.valid_form.clean()

        self.assertEqual(cleaned_data['username'], 'user')
        self.assertEqual(cleaned_data['first_name'], 'John')
        self.assertEqual(cleaned_data['last_name'], 'Doe')
        self.assertEqual(cleaned_data['password1'], 'password123')
        self.assertEqual(cleaned_data['password2'], 'password123')

    def test_clean_invalid_username(self) -> None:
        with self.assertRaises(ValidationError):
            self.invalid_username_form.clean()

    def test_clean_invalid_first_name(self) -> None:
        with self.assertRaises(ValidationError):
            self.invalid_first_name_form.clean()

    def test_clean_invalid_last_name(self) -> None:
        with self.assertRaises(ValidationError):
            self.invalid_first_name_form.clean()

    def test_clean_password_dont_match(self) -> None:
        with self.assertRaises(ValidationError):
            self.password_dont_match_form.clean()

    def test_clean_user_exists(self) -> None:
        with self.assertRaises(ValidationError):
            self.userprofile.save()
            self.user_already_exists_form.clean()

    def test_save(self) -> None:
        self.valid_form.is_valid()
        user = self.valid_form.save()

        self.assertTrue(CustomUser.objects.filter(username="test@gmail.com").exists())
        self.assertTrue(UserProfile.objects.filter(user=user.id).exists())
