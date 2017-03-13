import json

from django.shortcuts import render

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

def create_400_response(status_message, message):
    return Response({
        'status': status_message,
        'message': message
    }, status=status.HTTP_400_BAD_REQUEST)

class VerificationHelper:
    @staticmethod
    def verify_input_not_null(self, request):
        data = request.data

        email = self.request.user.email
        phone = self.request.user.phone
        verification_code = data.get('verification_code', None)

        valid_input = True
        message = ''

        # Make sure all required input has been provided
        if email is None:
            valid_input = False
            message = 'email missing'
        if phone is None:
            valid_input = False
            message = 'phone missing'
        if verification_code is None:
            valid_input = False
            message = 'verification_code missing'

        if not valid_input:
            return (False, "Missing input %s" % message)
        else:
            return (True, "All input is NOT None")

class VerifyPhone(APIView):
    serializer_class = AccountSerializer
    authentication_classes = [JSONWebTokenAuthenticationCookie]

    def post(self, request, format=None):
        email = None
        phone = None
        if self.request.user and self.request.user.is_authenticated():
            email = self.request.user.email
            phone = self.request.user.phone

        data = request.data
        verification_code = data.get('verification_code', None)

        correct_input_and_message = VerificationHelper.verify_input_not_null(self, request)

        valid_input = correct_input_and_message[0]
        message = correct_input_and_message[1]

        if not valid_input:
            return create_400_response('Invalid Input', message)

        # Verify  Email exists
        try:
            account = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return create_400_response('Invalid Input', 'Email does not exist')

        # Make sure Email and Phone match in the account
        user_phone = account.phone.raw_input
        if user_phone != phone:
            return create_400_response('Unauthorized', 'Phone and email do not match')

        # Make sure code matches
        phone_validated = account.validate_phone_auth_code(verification_code)
        if phone_validated:
            return Response({
                'status': "OK",
                "message": "Phone number has been verified"
            }, status=status.HTTP_200_OK)
        else:
            return create_400_response('Unauthorized', 'Code was incorrect')

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
            'message': serializer.errors
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
