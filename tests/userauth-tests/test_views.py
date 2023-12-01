from django.test import TestCase, Client

from apps.userauth.views import CustomLoginView, CustomSignupView
from apps.userauth.models import CustomUser


class TestCustomLoginView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email="test@gmai.com",
            password="mypassword123"
        )

    def test_form_invalid(self):
        response = self.client.post(path="/auth/login/", data={
            "username": "something wrong",
            "password": "something wrong too"
        })
        self.assertEqual(response, "expected string")


class TestCustomSignupView(TestCase):
    def setUp(self):
        pass

    def test_get(self):
        pass

    def test_post_valid_data(self):
        pass

    def test_post_invalid_data(self):
        pass
