from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class RegisterView(TemplateView):
    template_name = 'register/sign_up.html'

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        return context

class LoginView(TemplateView):
    template_name = 'login/login2.html'
