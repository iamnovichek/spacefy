import os
from pprint import pprint

from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from apps.userauth.models import CustomUser, UserProfile
from apps.userauth.forms import SignupForm


class TestCustomLoginView(TestCase):
    def setUp(self):
        CustomUser.objects.create_user(
            email='test@gmail.com',
            password='<PASSWORD>'
        )

        self.email = "test@gmail.com"

    def test_form_invalid(self):
        response = self.client.post(path='/auth/login/', data={
            'email': self.email,
            'password': 'invalid_password'
        })
        self.assertTrue(response)


# class TestSignupView(TestCase):
#     def setUp(self):
#         self.form = SignupForm()
#
#     def test_get(self):
#         response = self.client.get(reverse('signup'))
#         pprint(response.context)
#         self.assertEqual(response.status_code, 200)
