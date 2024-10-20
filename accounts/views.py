from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponse
from django.views import View, generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import LoginForm, SignupForm


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('pages:home')
        form = LoginForm()
        return render(request, template_name='accounts/login.html', context={'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.professor_verification:
                    login(request, user)
                    messages.success(request, f"Welcome {user.first_name}")
                    return redirect('panel:panel_home')
                else:
                    messages.info(request, "Professor verification failed.")
                    return redirect('accounts:login_view')
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('accounts:login_view')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('accounts:login_view')


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('pages:home')


class SignupView(generic.CreateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        form = SignupForm()
        return render(request, template_name='accounts/signup.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "registered successfully. Message sent for ICCI LAB's head for verification.")
            return redirect('accounts:login_view')
        else:
            messages.error(request, "oops you may entered invalid inputs try again.")
            return redirect('accounts:signup_view')


class CurrentView(generic.TemplateView):
    template_name = 'members/current.html'


class AlumniView(generic.TemplateView):
    template_name = 'members/Alumni.html'
