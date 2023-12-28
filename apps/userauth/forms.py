from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, UserProfile


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'email',
        'placeholder': 'Enter your email...',
        'id': 'email'
    }))

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'type': 'password',
            'class': 'form-control',
            'placeholder': 'Enter your password...',
            'id': 'password'
        }))


class SignupForm(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    password1 = forms.CharField(required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['email']

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        username = cleaned_data.get('username')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if len(username) < 2:
            raise ValidationError("Username should contain at least 2 characters!")

        if len(first_name) < 2:
            raise ValidationError("First name should contain at least 2 characters!")

        if len(last_name) < 2:
            raise ValidationError("Last name should contain at least 2 characters!")

        if password1 != password2:
            raise ValidationError("Password doesn't match!")

        if UserProfile.objects.filter(username=username).exists():
            raise ValidationError("Current username is already taken!")

    def save(self, commit=True):
        if commit:
            user = CustomUser.objects.create_user(
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password1']
            )

            UserProfile.objects.create(
                user=user,
                username=self.cleaned_data['username'],
                first_name=(self.cleaned_data['first_name'][0].capitalize() +
                            self.cleaned_data['first_name'][1:]),
                last_name=(self.cleaned_data['last_name'][0].capitalize() +
                           self.cleaned_data['last_name'][1:]),
            )

            return user
