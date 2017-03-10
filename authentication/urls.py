from django.conf.urls import url, include
from .views import AuthLogin, AuthLogout, VerifyPhone
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

urlpatterns = [
    url(r'^login/', AuthLogin.as_view()),
    url(r'^logout/', AuthLogout.as_view()),
    url(r'^token-refresh/', refresh_jwt_token),
    url(r'^token-verify/', verify_jwt_token),
    url(r'^verify-phone/', VerifyPhone.as_view())
]
