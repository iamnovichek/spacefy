import os

from datetime import datetime
from pprint import pprint
from django.core.exceptions import ValidationError
from django import forms
from django.forms import ClearableFileInput
from PIL import Image as I
from apps.userauth.models import UserProfile
from core import settings
from .models import Post, Gallery, Image, Story


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

    def save(self, commit=True):
        if commit:
            profile = UserProfile.objects.get(pk=self.instance.id)
            if self.cleaned_data['avatar']:
                if ("/media/" + str(self.cleaned_data['avatar'])) != profile.avatar.url:
                    try:
                        if profile.avatar.url != "/media/default.png":
                            os.remove(f"{os.getcwd()}/{profile.avatar.url}")
                    #  REWRITE THIS PART
                    except (FileNotFoundError, ValueError) as e:
                        print(e)
                    #  REWRITE THIS PART
                    if str(self.cleaned_data['avatar']).split(".")[-1] == "png":
                        img = I.open(fp=self.cleaned_data['avatar'])
                        img.resize(size=(200, 200))
                        img.convert('RGB').save(fp=settings.MEDIA_ROOT + "avatars/" + str(self.
                                           cleaned_data['avatar']).split('.')[0] + ".jpg")
                        profile.avatar = self.cleaned_data['avatar']
                    else:
                        img = I.open(fp=self.cleaned_data['avatar'])
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


class AddPostForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={"cols": "30", "rows": "2"}))

    class Meta:
        model = Post
        fields = ['text']

    def save(self, commit=True):
        if commit:
            post = Post.objects.create(
                user=self.instance,
                text=self.cleaned_data['text'],
            )

            return post


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class AddPhotoForm(forms.ModelForm):
    image = MultipleFileField()

    class Meta:
        model = Gallery
        fields = ['description']

    def save(self, commit=True):
        result = super().save(commit=commit)
        if commit:
            for image in self.cleaned_data['image']:
                Image(gallery=result, image=image).save()
            return result


class AddStoryForm(forms.ModelForm):
    story = forms.FileField(required=True, widget=forms.FileInput)

    class Meta:
        model = Story
        fields = ['story']
