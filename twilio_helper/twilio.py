from django.conf import settings
from twilio.rest import TwilioRestClient
from authentication.models import Account
from django.conf import settings

def generate_client():
    return TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

client = generate_client()

def send_message(to, from_, body):
    client.messages.create(
        to=to,
        from_=from_,
        body=body
    )

def send_sms_auth(account):
    message = "Welcome to Alpacka! Your code is %d" % account.phone_auth_code
    send_message(account.phone.raw_input, settings.TWILIO_PHONE, message)
