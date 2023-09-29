import random
import uuid
from django.conf import settings

from .tasks import client

def generate_sms_code () -> str:
    return ''.join([str(random.randint(0, 9)) for i in range(settings.SMS_CODE_LENGTH)])


def normalize_phone_number (phone: str) -> str:
    return phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')


def generate_email_verification_token() -> str:
    return str(uuid.uuid4())


def phone_number_is_valid(phone: str) -> (bool, str):
    look_up = client.lookups.v2.phone_numbers(phone).fetch()

    return (look_up.valid, look_up.phone_number)