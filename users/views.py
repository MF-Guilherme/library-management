from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import EmailAuthenticationForm, EmailUserCreationForm


class CustomLoginView(LoginView):
    authentication_form = EmailAuthenticationForm


class SignUpView(generic.CreateView):
    form_class = EmailUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
 
