from calendar import c
from http import client
import random
from django.conf import settings
from twilio.rest import Client

class Messhandler:
    phone_number = None
    otp          = None
    def __init__(self, phone_number, otp) -> None:
        self.phone_number = phone_number
        self.otp          = otp

    def send_otp_to_phone(self):
        client = Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)

        message = client.messages.create(body=f'your otp is{self.otp}',from_='+18597651446',to=self.phone_number)

        print(message.sid)

        
# def otp(request):
#     global num1
#     global phone
#     # if request.user.is_authenticated:
#     #     return redirect(home)

#     if request.method == 'POST':
#         phone = request.POST['phone']
#         num1 = random.randint(1000, 9999)
#         print(num1)
#         account_sid = '#'
#         auth_token = '#'
#         client = Client(account_sid, auth_token)
#         message = client.messages.create(
#             body='otp : ' + str(num1),
#             from_='[+][1][#]',
#             to='[+][91]' + str([phone])
#         )
#         return redirect(otp_verify)

#     return render(request, 'otp_login.html')
