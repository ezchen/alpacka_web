from django.shortcuts import render
from django.views.generic.base import TemplateView
from rest_framework import generics
from django.http import HttpResponseRedirect

from login_register.serializers import MessageSerializer

# Create your views here.
class RegisterView(TemplateView):
    template_name = 'register/sign_up.html'

class LoginView(TemplateView):
    template_name = 'login/login2.html'

class LandingPageView(TemplateView):
    template_name = 'landing/index25.html'

class MessageCreateView(generics.CreateAPIView):
    authentication_classes = []
    serializer_class = MessageSerializer
