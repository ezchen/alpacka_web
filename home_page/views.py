from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from authentication.jwt_authentication import JSONWebTokenAuthenticationCookie

# Create your views here.
class HomePageView(TemplateView):
    template_name = "my_tasks.html"
    authentication_classes = [JSONWebTokenAuthenticationCookie]

class PostTaskView(TemplateView):
    template_name = "post_task.html"
    authentication_classes = [JSONWebTokenAuthenticationCookie]

class AllTasksView(TemplateView):
    template_name = "tasks.html"
    authentication_classes = [JSONWebTokenAuthenticationCookie]

class AcceptedTasksView(TemplateView):
    template_name = "accepted_tasks.html"
    authentication_classes = [JSONWebTokenAuthenticationCookie]
