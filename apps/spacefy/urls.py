from django.urls import path
from django.views.generic import TemplateView

from .views import MySpaceView

urlpatterns = [
    path('', TemplateView.as_view(template_name='apps.spacefy/home.html'), name='home'),
    path('my-space', MySpaceView.as_view(), name='my-space')
]
