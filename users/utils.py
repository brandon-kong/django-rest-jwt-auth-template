import datetime
from random import randint

from django.conf import settings
from django.utils.timezone import make_aware
from typing import Literal, TypedDict
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_200_OK

from .models import (
    PhoneVerificationToken,
)

from twilio.rest import Client

TWILIO_CLIENT = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

response_types = TypedDict(
    'response_types',
   {
       "status_code": int,
        "error_type": str,
        "error_message": str,
        "detail": dict,
        "http_status": HTTP_400_BAD_REQUEST | HTTP_401_UNAUTHORIZED | HTTP_500_INTERNAL_SERVER_ERROR,
    }
)

error_types = {
    'user_already_exists': 'The provided user already exists!',
    'invalid_email_address': 'The provided email address is not valid!',
    'invalid_credentials': 'The provided email/phone and/or password are not valid!',
    'invalid_phone_number': 'The provided phone number is not valid!',
    'user_doesnt_exist': 'The provided user does not exist!',
    'user_already_verified': 'The provided user is already verified!',
    'invalid_token': 'The provided token is not valid!',
    'invalid_request': 'The provided request is not valid!',
    'invalid_user': 'The provided user is not valid!',
    'invalid_password': 'The provided password is not valid!',
    'invalid_email': 'The provided email is not valid!',
    'invalid_phone': 'The provided phone is not valid!',
    'invalid_username': 'The provided username is not valid!',
    'invalid_first_name': 'The provided first name is not valid!',
    'invalid_last_name': 'The provided last name is not valid!',
    'invalid_birth_date': 'The provided birth date is not valid!',
}

http_status_codes = {
    200: HTTP_200_OK,
    400: HTTP_400_BAD_REQUEST,
    401: HTTP_401_UNAUTHORIZED,
    500: HTTP_500_INTERNAL_SERVER_ERROR,
}

def generate_error_response(info: response_types):
    return Response({
        "detail": info.get('detail'),
        "status_code": info.get('status_code'),
        "error_type": info.get('error_type'),
        "error_message": error_types[info.get('error_type')],
    }, status=http_status_codes.get(info.get('status_code')) or HTTP_500_INTERNAL_SERVER_ERROR)

def generate_success_response(info: response_types):
    return Response({
        "detail": info.get('detail'),
         "status_code": info.get('status_code'),
    }, status=HTTP_200_OK)

def send_sms(phone: str, message: str):
    return TWILIO_CLIENT.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone
    )

def generate_sms_token():
    rand = randint(100000, 999999)
    print(rand)

    if PhoneVerificationToken.objects.filter(token=rand).exists():
        return generate_sms_token()

    return rand

def get_time_now():
    return make_aware(datetime.datetime.now())

def validate_phone_number(phone: str) -> bool:
    if not phone:
        return False

    phone_number = TWILIO_CLIENT.lookups.v2.phone_numbers(phone).fetch()
    print(phone_number)

    if not phone_number.valid:
        return False

    return True