from threading import Thread

from django.conf import settings
from django.core.mail import send_mail

from twilio.rest import Client

client = Client(
    settings.TWILIO_ACCOUNT_SID,
    settings.TWILIO_AUTH_TOKEN,
)

class SendEmailThread(Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.html_content = html_content
        self.recipient_list = recipient_list
        Thread.__init__(self)

    def run(self):
        send_mail(
            subject=self.subject,
            message='',
            html_message=self.html_content,
            recipient_list=self.recipient_list,
            from_email=settings.EMAIL_HOST_USER,
        )

def send_email(subject, html_content, recipient_list):
    SendEmailThread(subject, html_content, recipient_list).start()

class SendPhoneCodeThread(Thread):
    def __init__(self, phone, code):
        self.phone = phone
        self.code = code
        Thread.__init__(self)

    def run(self):
        
        if settings.SEND_SMS_TEXT:
            client.messages.create(
                body=f'Your code is {self.code}',
                from_=settings.TWILIO_PHONE_NUMBER,
                to=self.phone,
            )

def send_phone_code(phone, code):
    SendPhoneCodeThread(phone, code).start()

class CallPhoneWithCodeThread(Thread):
    def __init__(self, phone, code):
        self.phone = phone
        self.code = code
        Thread.__init__(self)

    def run(self):
        
        # format code with spaces between each number
        self.code = '. '.join(self.code)

        if settings.SEND_SMS_CALL:
            client.calls.create(
                twiml=f'<Response><Say>Your,, code, is. {self.code}</Say><Pause></Pause><Say>Again,, Your, code, is. {self.code}</Say><Pause></Pause><Say>Thank you, and stay cool. </Say></Response>',
                from_=settings.TWILIO_PHONE_NUMBER,
                to=self.phone,
            )

def call_phone_with_code(phone, code):
    CallPhoneWithCodeThread(phone, code).start()