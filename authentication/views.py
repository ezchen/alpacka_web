import json

from django.shortcuts import render

from authy.api import AuthyApiClient

from overrides import overrides

from rest_framework import permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework_jwt.settings import api_settings

from authentication.models import Account
from authentication.permissions import IsAccountOwner, IsPhoneVerified, IsEmailVerified
from authentication.serializers import AccountSerializer
from authentication.jwt_authentication import JSONWebTokenAuthenticationCookie

from django.contrib.auth import authenticate

from django.http import HttpResponseRedirect

from django.views.generic.base import TemplateView

from twilio_helper import twilio



# Create your views here.
def setCookie(account, response):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(account)
    token = jwt_encode_handler(payload)
    response.set_cookie('jwt', token, httponly=True)

class VerifyPhone(APIView):
    serializer_class = AccountSerializer
    authentication_classes = [JSONWebTokenAuthenticationCookie]

    def post(self, request, format=None):
        data = request.data

        email = data.get('email', None)
        phone = data.get('phone', None)
        verification_code = data.get('verification_code', None)

        valid_input = True
        message = ''

        # Make sure all required input has been provided
        if email is None:
            valid_input = False
            message = 'email missing'
        if phone is None:
            valid_input = False
            'phone missing'
        if verification_code is None:
            valid_input = False
            'verification_code missing'

        if not valid_input:
            return Response({
                'status': 'Unauthorized',
                'message': "Missing input: %s" % message
            }, status=status.HTTP_400_BAD_REQUEST)

        # Verify  Email exists
        try:
            account = Account.objects.get(email=email)
        except Account.DoesNotExist:
            valid_input = False
            return Response({
                'status': 'Unauthorized',
                'message': "Email does not exist"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Make sure Email and Phone match in the account
        user_phone = account.phone.raw_input
        if user_phone != phone:
            valid_input = False
            return Response({
                'status': 'Unauthorized',
                'message': 'Phone and Email do not match'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Make sure code matches
        phone_validated = account.validate_phone_auth_code(verification_code)
        import pdb; pdb.set_trace()

        if phone_validated:
            return Response({
                'status': "OK",
                "message": "Phone number has been verified"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': "Auth code is incorrect"
            }, status=status.HTTP_400_BAD_REQUEST)

class AuthLogout(APIView):
    serializer_class = AccountSerializer
    authentication_classes = [JSONWebTokenAuthenticationCookie]

    def post(self, request, format=None):
        response = HttpResponseRedirect('/login/')
        response.delete_cookie('jwt')
        return response

class AuthLogin(APIView):
    serializer_class = AccountSerializer
    authentication_classes = []

    def post(self, request, format=None):
        data = request.data

        email = data.get('email', None)
        password = data.get('password', None)
        print(email)
        print(password)

        account = authenticate(email=email, password=password)

        if account is not None:
            serialized = AccountSerializer(account)
            response = Response(serialized.data)
            setCookie(account, response)
            return response
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)

class AccountViewSet(viewsets.ModelViewSet):
    lookup_field = 'email'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = []

    @overrides
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), IsAccountOwner(),)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Creates the account
            account = serializer.save()
            data = serializer.data
            response = Response(serializer.data, status=status.HTTP_201_CREATED)

            twilio.send_sms_auth(account)
            # Set JWT for authentication
            setCookie(account, response)


            return response

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, email=None):
        if self.request.user and not self.request.user.is_anonymous():
            serializer = self.serializer_class(self.request.user)

            return Response(serializer.data)
        return Response({
            'status': 'Bad request',
            'message': 'You must be logged in to view this information'
        }, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        return Response({
            'status': 'Bad request',
            'message': 'List not allowed'
        }, status=status.HTTP_400_BAD_REQUEST)
