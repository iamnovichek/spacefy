from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('login/', TemplateView.as_view(template_name='apps.userauth/login.html'), name='login'),
    path('signup/', TemplateView.as_view(template_name='apps.userauth/signup.html'), name='signup'),
]
