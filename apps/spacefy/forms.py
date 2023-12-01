import os

from datetime import datetime

from django.core.exceptions import ValidationError
from django import forms
from django.forms import ClearableFileInput
from PIL import Image
from apps.userauth.models import UserProfile


class CreateMySpaceForm(forms.ModelForm):
    username = forms.CharField(min_length=2, required=True)
    first_name = forms.CharField(min_length=2, required=True)
    last_name = forms.CharField(min_length=2, required=True)

    class Meta:
        model = UserProfile
        fields = [
            'username',
            'first_name',
            'last_name',
        ]

    def clean(self):
        cleaned_data = super(CreateMySpaceForm, self).clean()
        username = cleaned_data.get('username')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if len(username) < 2:
            raise ValidationError("Username should contain at least 2 characters!")

        if len(first_name) < 2:
            raise ValidationError("First name should contain at least 2 characters!")

        if len(last_name) < 2:
            raise ValidationError("Last name should contain at least 2 characters!")

        if UserProfile.objects.filter(username=username).exists():
            raise ValidationError("Current username is already taken!")

        return cleaned_data

    def save(self, commit=True):
        if commit:
            profile = UserProfile.objects.create(
                user=self.instance,
                username=self.cleaned_data['username'],
                slug=self.cleaned_data['username'],
                first_name=(self.cleaned_data['first_name'][0].capitalize() +
                            self.cleaned_data['first_name'][1:]),
                last_name=(self.cleaned_data['last_name'][0].capitalize() +
                           self.cleaned_data['last_name'][1:])
            )

            return profile


class EditMySpaceForm(forms.ModelForm):
    avatar = forms.ImageField(required=False, widget=forms.FileInput)
    username = forms.CharField(min_length=2, required=True)
    first_name = forms.CharField(min_length=2, required=True)
    last_name = forms.CharField(min_length=2, required=True)
    description = forms.Textarea()

    class Meta:
        model = UserProfile
        fields = [
            'username',
            'avatar',
            'first_name',
            'last_name',
            'description'
        ]

    def clean(self):
        userprofile = UserProfile.objects.get(user=self.instance.user)
        cleaned_data = super(EditMySpaceForm, self).clean()
        username = cleaned_data.get('username')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if len(username) < 2:
            raise ValidationError("Username should contain at least 2 characters!")

        if len(first_name) < 2:
            raise ValidationError("First name should contain at least 2 characters!")

        if len(last_name) < 2:
            raise ValidationError("Last name should contain at least 2 characters!")

        if userprofile.username != username:
            if UserProfile.objects.filter(username=username).exists():
                raise ValidationError("Current username is already taken!")

        return cleaned_data

    def is_valid(self):
        res = super().is_valid()
        if not res:
            print(self.errors)
            return res
        return res

    def save(self, commit=True):
        if commit:
            profile = UserProfile.objects.get(pk=self.instance.id)
            if self.cleaned_data['avatar']:
                if ("/media/" + str(self.cleaned_data['avatar'])) != profile.avatar.url:
                    try:
                        if profile.avatar.url != "/media/default.png":
                            os.remove(f"{os.getcwd()}/{profile.avatar.url}")
                    except (FileNotFoundError, ValueError) as e:
                        print(e)

                    img = Image.open(fp=self.cleaned_data['avatar'])
                    img.resize(size=(200, 200))
                    img.save(fp=self.cleaned_data['avatar'])
                    profile.avatar = self.cleaned_data['avatar']

            profile.username = self.cleaned_data['username']
            profile.first_name = (self.cleaned_data['first_name'][0].capitalize() +
                                  self.cleaned_data['first_name'][1:])
            profile.last_name = (self.cleaned_data['last_name'][0].capitalize() +
                                 self.cleaned_data['last_name'][1:])
            profile.description = self.cleaned_data['description']
            profile.save()
