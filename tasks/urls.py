from django.conf.urls import url

from . import views

app_name = 'tasks'
urlpatterns = [
    url(r'tasks', views.CourierTaskDetail.as_view())
]
