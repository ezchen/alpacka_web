from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect

# Create your views here.
class RegisterView(TemplateView):
    template_name = 'register/sign_up.html'

class LoginView(TemplateView):
    template_name = 'login/login2.html'
