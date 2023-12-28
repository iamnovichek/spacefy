from django.contrib.auth.views import (LogoutView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from django.urls import path

from .views import CustomLoginView, SignupView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', PasswordResetView.as_view(template_name='apps.userauth/password_reset.html'),
         name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='apps.userauth/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='apps.userauth/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='apps.userauth/password_reset_complete.html'),
         name='password_reset_complete'),
]
