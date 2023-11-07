from django.shortcuts import render
from django.views import View


class MySpaceView(View):
    template_name = 'apps.spacefy/my-space.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
