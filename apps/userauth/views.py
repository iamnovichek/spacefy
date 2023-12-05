from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomSignupForm


class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    template_name = 'apps.userauth/login.html'
    success_url = "home"

    def form_invalid(self, form):
        messages.error(self.request, message="Please enter a correct email and password.Note that both fields may be "
                                             "case-sensitive. (You can also try to login with google)")
        return self.render_to_response(self.get_context_data(form=form))


class CustomSignupView(CreateView):
    form_class = CustomSignupForm
    success_url = 'home'
    template_name = 'apps.userauth/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect(self.success_url)

        return render(request, self.template_name, context={'form': form})
