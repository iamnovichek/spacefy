from pprint import pprint

from django.http import JsonResponse
from django.urls import reverse_lazy as _
from django.views.generic import UpdateView, CreateView, TemplateView
from django.shortcuts import render, redirect
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from core import settings
from apps.userauth.models import CustomUser, UserProfile
from .forms import (EditMySpaceForm, CreateMySpaceForm,
                    AddPostForm, AddPhotoForm, AddStoryForm)
from .models import Post, Gallery, Image, Friend

from django.contrib import messages

from .tasks import remove_story


class CreateMySpaceView(CreateView):
    template_name = 'apps.spacefy/create-profile.html'
    success_url = 'my-space'
    form_class = CreateMySpaceForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})


class MySpaceView(View):
    template_name = 'apps.spacefy/my-space.html'
    user_has_not_profile_template = "apps.spacefy/no-profile.html"

    def get(self, request, *args, **kwargs):
        try:
            if CustomUser.objects.get(email=str(request.user)).userprofile:
                total_photos_number = 0
                for gallery in Gallery.objects.filter(user_id=request.user):
                    total_photos_number += Image.objects.filter(gallery_id=gallery.id).count()
                return render(request, self.template_name, context={
                    'posts': Post.objects.filter(user_id=request.user).count(),
                    'photos': total_photos_number,
                    'friends': Friend.objects.filter(user_id=request.user).count()
                })
        except ObjectDoesNotExist:
            return render(request, self.user_has_not_profile_template)


class EditMySpaceView(UpdateView):
    form_class = EditMySpaceForm
    template_name = "apps.spacefy/edit.html"
    slug_url_kwarg = 'slug'
    success_url = _('my-space')

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user.userprofile)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST,
                               request.FILES,
                               instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})


class AddPostView(CreateView):
    template_name = 'apps.spacefy/add-post.html'
    form_class = AddPostForm
    success_url = _('my-space')

    def form_valid(self, form):
        form.instance = self.request.user
        return super().form_valid(form)


class MyPostsView(View):
    template_name = 'apps.spacefy/posts.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={
            "posts": Post.objects.filter(user_id=request.user)[::-1],
        })


class AddPhotoView(CreateView):
    template_name = 'apps.spacefy/add-photo.html'
    form_class = AddPhotoForm
    success_url = _('my-space')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, message='Upload at least one photo!')
        return super().form_invalid(form)


class MyPhotosView(View):
    template_name = 'apps.spacefy/photos.html'

    def get(self, request, *args, **kwargs):
        photos = []
        for gallery in Gallery.objects.filter(user_id=request.user)[::-1]:
            if Image.objects.filter(gallery_id=gallery.id).count() == 1:
                photos.append(
                    {
                        "multiple": False,
                        "photo": settings.MEDIA_URL + Image.objects.
                        get(gallery_id=gallery.id).image.name,
                        "description": gallery.description,
                        "created": str(gallery.creation_date.date())
                    }
                )
            else:
                photos.append(
                    {
                        "multiple": True,
                        "photos": [settings.MEDIA_URL + inst.image.name
                                   for inst in Image.objects.
                                   filter(gallery_id=gallery.id)],
                        "description": gallery.description,
                        "created": str(gallery.creation_date.date())
                    }
                )
        return render(request, self.template_name, context={"photos": photos})


class AddStoryView(CreateView):
    template_name = 'apps.spacefy/add-story.html'
    form_class = AddStoryForm
    success_url = _('my-space')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, context={"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        form.instance.user = request.user
        if form.is_valid():
            result = form.save()
            remove_story.apply_async(args=[str(result.story)],
                                     countdown=settings.STORY_LIFE_TIME)
            return redirect(self.success_url)
        return render(request, self.template_name, context={"form": form})


class SearchUsersAjaxView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        usernames = [str(user.username) for user in
                     UserProfile.objects.filter(
                         username__icontains=request.GET.get("data", ""))] \
                     if request.GET.get("data") else ""
        if request.user.userprofile.username in usernames:
            usernames.remove(request.user.userprofile.username)

        return JsonResponse({"usernames": usernames})


class AnotherSpaceView(TemplateView):
    template_name = 'apps.spacefy/another-space.html'

    def get_context_data(self, **kwargs):
        result = super().get_context_data()
        profile = UserProfile.objects.get(username=kwargs['username'])
        user = profile.user
        result["username"] = profile.username
        result["full_name"] = profile.first_name + " " + profile.last_name
        result["avatar"] = profile.avatar.url
        result["description"] = profile.description
        result["posts"] = Post.objects.filter(user_id=user).count()
        photos = 0
        for gallery in Gallery.objects.filter(user_id=user):
            photos += Image.objects.filter(gallery_id=gallery.id).count()
        result['photos'] = photos
        result['friends'] = Friend.objects.filter(user_id=user).count()
        result['is_friend'] = (
            Friend.objects.filter(user_id=self.request.user, friend_id=user).exists())

        return result


class AnotherSpacePostsView(TemplateView):
    template_name = 'apps.spacefy/another-space-posts.html'

    def get_context_data(self, **kwargs):
        result = super().get_context_data()
        profile = UserProfile.objects.get(username=kwargs['username'])
        result["posts"] = Post.objects.filter(user_id=profile.user)[::-1]
        result["username"] = profile.username
        result["avatar"] = profile.avatar.url
        return result


class AnotherSpacePhotosView(TemplateView):
    template_name = 'apps.spacefy/another-space-photos.html'

    def get_context_data(self, **kwargs):
        result = super().get_context_data()
        profile = UserProfile.objects.get(username=kwargs['username'])
        result["username"] = profile.username
        result["avatar"] = profile.avatar.url
        photos = []
        for gallery in Gallery.objects.filter(user_id=profile.user)[::-1]:
            if Image.objects.filter(gallery_id=gallery.id).count() == 1:
                photos.append(
                    {
                        "multiple": False,
                        "photo": settings.MEDIA_URL + Image.objects.
                        get(gallery_id=gallery.id).image.name,
                        "description": gallery.description,
                        "created": str(gallery.creation_date.date())
                    }
                )
            else:
                photos.append(
                    {
                        "multiple": True,
                        "photos": [settings.MEDIA_URL + inst.image.name
                                   for inst in Image.objects.
                                   filter(gallery_id=gallery.id)],
                        "description": gallery.description,
                        "created": str(gallery.creation_date.date())
                    }
                )
        result["photos"] = photos
        return result


class AddToFriendsAjaxView(TemplateView):
    def post(self, request, *args, **kwargs):
        Friend.objects.create(
            user=request.user,
            friend=UserProfile.objects.
            get(username=request.POST["username"]).user
        )
        return JsonResponse({"result": "success"})


class RemoveFromFriendsAjaxView(TemplateView):
    def post(self, request, *args, **kwargs):
        Friend.objects.get(
            user_id=request.user,
            friend_id=UserProfile.objects.
            get(username=request.POST["username"]).user
        ).delete()
        return JsonResponse({"result": "success"})


class MySpaceFriendsView(TemplateView):
    template_name = "apps.spacefy/my-space-friends.html"

    def get_context_data(self, **kwargs):
        result = super().get_context_data()

        result["friends"] = [UserProfile.objects.get(user=friend.friend)
                             for friend in Friend.objects.
                             filter(user_id=self.request.user)]

        return result


class AnotherSpaceFriendsView(TemplateView):
    template_name = "apps.spacefy/another-space-friends.html"

    def get_context_data(self, **kwargs):
        result = super().get_context_data()

        result["friends"] = [UserProfile.objects.get(user=friend.friend)
                             for friend in Friend.objects.
                             filter(user_id=UserProfile.objects.
                                    get(username=kwargs["username"]).user)]

        return result
