import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings

client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN )
verify = client.verify.services(settings.SERVICE_ID)


def send(phone):
    verify.verifications.create(to=str('+91')+phone, channel='sms')


def check(phone, code):
    try:
        result = verify.verification_checks.create(to=str('+91')+phone, code=code)
        print(result)
    except TwilioRestException:
        print('noooooooooooooooooooooooooooooooo')
        return False
    
    return result.status == 'approved'