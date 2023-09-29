from typing import TypedDict
from rest_framework.response import Response

from rest_framework.status import (
    HTTP_500_INTERNAL_SERVER_ERROR, 
    HTTP_401_UNAUTHORIZED, 
    HTTP_400_BAD_REQUEST, HTTP_200_OK, 
    HTTP_204_NO_CONTENT, 
    HTTP_201_CREATED
)

from uuid import UUID

response_types = TypedDict(
    'response_types',
   {
       "status_code": int,
        "error_type": str,
        "error_message": str,
        "detail": dict,
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
    'invalid_country_code': 'The provided country code is not valid!',
    'invalid_birth_date': 'The provided birth date is not valid!',
    'invalid_id': 'The provided id is not valid!',
    "token_attempts_exceeded": "The provided token attempts exceeded!",
    'token_expired': 'The provided token is expired!',
    'token_not_found': 'The provided token is not found!',
    'token_not_verified': 'The provided token is not verified!',
}

http_status_codes = {
    200: HTTP_200_OK,
    201: HTTP_201_CREATED,
    204: HTTP_204_NO_CONTENT,
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
         "status_code": info.get('status_code') or 200,
    }, status=HTTP_200_OK)

def validate_uuid4(uuid_string):
    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
        return False

    return val.hex == uuid_string.replace('-', '')