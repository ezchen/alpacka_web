from django.test import TestCase
from authentication.models import Account
from django.test import Client
from rest_framework import status
from phonenumber_field.modelfields import PhoneNumberField


# Create your tests here.
testEmail = "phoneVerificationTest@test.com"
testFirstName = "first_name"
testLastName = "last_name"
testPassword = "password"
testPhone = "+19174765509"

def create_default_account():
    client = Client()

    data = {
        "first_name": testFirstName,
        "last_name": testLastName,
        "email": testEmail,
        "password": testPassword,
        "phone": testPhone
    }

    response = client.post('/api/v1/accounts/', data)
    data = response.data
    account = Account.objects.get(email=testEmail)

def get_default_account():
    return Account.objects.get(email=testEmail)

def login_default_account(client):
    data = {
        'email': testEmail,
        'password': testPassword
    }
    return client.post('/api/v1/auth/login/', data)


class AccountPhoneVerificationTestCase(TestCase):


    def setUp(self):
        # Create an account with a registered twilio number
        create_default_account()

    def tearDown(self):
        account = Account.objects.get(email=testEmail)
        account.delete()


    def test_phone_auth_code(self):
        account = Account.objects.get(email=testEmail)

        auth_code = account.set_phone_auth_code()

        self.assertEqual(auth_code, account.phone_auth_code)

        validated_code = account.validate_phone_auth_code(auth_code)

        self.assertTrue(validated_code)
        self.assertTrue(account.phone_auth_code)
        self.assertIsNotNone(account.phone_verification_date)

# Client tests
class AccountRegisterClientTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        try:
            account = Account.objects.get(email=testEmail)

            account.delete()
        except Account.DoesNotExist:
            return

    def test_register(self):
        client = Client()

        data = {
            "first_name": testFirstName,
            "last_name": testLastName,
            "email": testEmail,
            "password": testPassword,
            "phone": testPhone
        }

        response = client.post('/api/v1/accounts/', data)
        data = response.data
        account = Account.objects.get(email=testEmail)

        self.assertEqual(data['email'],testEmail)
        self.assertEqual(data['first_name'], testFirstName)
        self.assertEqual(data['last_name'], testLastName)
        self.assertEqual(data['phone'], testPhone)
        self.assertFalse('password' in data)

        self.assertFalse(account.phone_verified)
        self.assertFalse(account.email_verified)
        self.assertIsNotNone(account.phone_auth_code)

        account.delete()

    def test_login(self):
        client = Client()

        data = {
        "email": testEmail,
        "password": testPassword
        }

        response = client.post('/api/v1/auth/login', data)
        self.assertEqual(data['email'], testEmail)
        print("LOGIN")

class AccountPhoneClientVerificationTest(TestCase):
    def setUp(self):
        pass

    def register_default_account(self, client):
        create_default_account()
        account = get_default_account()
        account.phone_auth_code = 9999
        account.save()
        response = login_default_account(client)
        print(response)

    def test_verify_phone_post_request(self):
        client = Client()
        self.register_default_account(client)

        account = Account.objects.get(email=testEmail)
        email = account.email
        phone = account.phone.raw_input
        auth_code = account.phone_auth_code

        data = {
            "email": email,
            "phone": phone,
            "verification_code": auth_code
        }
        response = client.post('/api/v1/auth/verify-phone/', data)


        updated_account = Account.objects.get(email=testEmail)


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(updated_account)
        self.assertIsNotNone(updated_account.phone_verification_date)

        account.delete()

    def test_invalid_input_phone_post_request(self):
        c = Client()
        self.register_default_account(c)

        account = Account.objects.get(email=testEmail)

        # Test Missing Input
        account = Account.objects.get(email=testEmail)
        email = account.email
        phone = account.phone.raw_input
        auth_code = account.phone_auth_code

        # missing verification code
        data3 = {
            "email": email,
            "phone": phone
        }

        response = c.post('/api/v1/auth/verify-phone/', data3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # wrong verification code
        data5 = {
            "email": email,
            "phone": phone,
            "verification_code": 1234
        }

        response = c.post('/api/v1/auth/verify-phone/', data5)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        account.delete()
