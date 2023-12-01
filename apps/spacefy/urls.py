from django.urls import path
from django.views.generic import TemplateView

from .views import MySpaceView, EditMySpaceView, CreateMySpaceView

urlpatterns = [
    path('', TemplateView.as_view(template_name='apps.spacefy/home.html'), name='home'),
    path('my-space/', MySpaceView.as_view(), name='my-space'),
    path('edit-my-space/<slug:slug>/', EditMySpaceView.as_view(), name='edit-my-space'),
    path('create-profile/', CreateMySpaceView.as_view(), name='create-profile'),
]
