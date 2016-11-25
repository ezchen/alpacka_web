"""alpacka_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework_nested import routers
from authentication.views import AccountViewSet
from tasks.views import AccountTasksViewSet, TaskViewSet
from django.conf.urls.static import static



router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'tasks', TaskViewSet)
router.register('accounts/my_account/my_tasks', AccountTasksViewSet)

urlpatterns = [
    url(r'^', include('home_page.urls')),
    url(r'^', include('login_register.urls')),
    url(r'^admin/', admin.site.urls),

    url(r'^api/v1/', include(router.urls)),

    url(r'^api/v1/courier/', include('tasks.urls')),

    # login, token refresh, verify token
    url(r'^api/v1/auth/', include('authentication.urls')),

    # TODO: make catchall route  url('^.*$', IndexView.as_view(), name='index'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
