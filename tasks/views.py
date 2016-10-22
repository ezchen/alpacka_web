from django.shortcuts import render
from django.http import HttpResponse

from .models import Task

def index(request):
    latest_tasks = Task.objects.order_by('-pub_date')[:20]
    context = {'latest_tasks': latest_tasks}
    return render(request, 'tasks/index.html', context)
