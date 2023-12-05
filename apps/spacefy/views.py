from pprint import pprint

from django.views.generic import UpdateView, CreateView
from django.shortcuts import render, redirect
from django.views import View
from django.core.exceptions import ObjectDoesNotExist

from .forms import EditMySpaceForm, CreateMySpaceForm, AddPostForm
from apps.userauth.models import CustomUser


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
                return render(request, self.template_name)
        except ObjectDoesNotExist:
            return render(request, self.user_has_not_profile_template)


class EditMySpaceView(UpdateView):
    form_class = EditMySpaceForm
    template_name = "apps.spacefy/edit.html"
    slug_url_kwarg = 'slug'
    success_url = 'my-space'

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
    success_url = 'my-space'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})
