from django.conf.urls import url

from . import views
from .views import HomePageView
from .views import PostTaskView
from .views import AllTasksView
from .views import AcceptedTasksView

app_name = 'home_page'
urlpatterns = [
    #url(r'^dashboard/', HomePageView.as_view(), name='Home'),
    #url(r'^post_task/', PostTaskView.as_view(), name="post_task"),
    #url(r'^tasks/', AllTasksView.as_view(), name="all_tasks"),
    #url(r'^accepted_tasks/', AcceptedTasksView.as_view(), name="accepted_tasks")
]
