from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import CustomLoginView, CustomSignupView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', CustomSignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout')
]
