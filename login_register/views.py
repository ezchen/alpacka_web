from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect

# Create your views here.
class RegisterView(TemplateView):
    template_name = 'register/sign_up.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/dashboard')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

class LoginView(TemplateView):
    template_name = 'login/login2.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/dashboard')
        return super(LoginView, self).dispatch(request, *args, **kwargs)
