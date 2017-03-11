from django.conf.urls import url

from . import views
from .views import RegisterView
from .views import LoginView
from .views import MessageCreateView

app_name = 'login_register'
urlpatterns = [
    url(r'^register/', RegisterView.as_view(), name='register'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^message/', MessageCreateView.as_view(), name='create_message')
]
