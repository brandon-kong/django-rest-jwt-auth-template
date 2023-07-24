from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from twilio.rest import Client

from .models import (
    User,
    PhoneVerificationToken
)

from .utils import (
    generate_error_response, 
    generate_success_response,
    send_sms,
    generate_sms_token
)

from .serializers import (
    UserEmailSerializer, 
    UserPhoneSerializer, 
    PhoneTokenPairSerializer
)

"""

# Sample Success Response
{
    "detail": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    },
    "status_code": 200,
}

# Sample Error Response

{
    "detail": {
        "email": [
            "This field may not be blank."
        ],
        "password": [
            "This field may not be blank."
        ]
    },
    "status_code": 500,
    "error_type": "invalid_credentials",
    "error_message": "The provided email and/or password are not correct!"
}
"""

class HelloView(APIView):
    def get(self, request):
        return Response({"message": "Hello, world!"})
    
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Hello, world!"})
    

class CreateUserWithEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        email = data.get('email')
        
        if not email:
            return generate_error_response ({
                "status_code": 400,
                "error_type": "invalid_email_address",
                "detail": {
                    "email": [
                        "This field may not be blank."
                    ],
                }
            })
        
        if email:
            if User.objects.filter(email=email).exists():
                return generate_error_response ({
                    "status_code": 400,
                    "error_type": "user_already_exists",
                    "detail": {
                        "email": [
                            "This email is already in use."
                        ]
                    }
                })
            
            serializer = UserEmailSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()

                # generate token
                
                refresh = RefreshToken.for_user(user)

                return generate_success_response ({
                    "status_code": 200,
                    "detail": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                })
            else:
                return generate_error_response ({
                    "status_code": 500,
                    "error_type": "invalid_request",
                    "detail": serializer.errors
                })
            
class CreateUserWithPhoneView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        phone = data.get('phone')
        
        if not phone:
            return generate_error_response ({
                "status_code": 400,
                "error_type": "invalid_phone_number",
                "detail": {
                    "phone": [
                        "This field may not be blank."
                    ],
                }
            })
        
        if User.objects.filter(phone=phone).exists():
            return generate_error_response ({
                "status_code": 400,
                "error_type": "user_already_exists",
                "detail": {
                    "phone": [
                        "This phone is already in use."
                    ]
                }
            })
        
        # TODO: Validate phone number

        serializer = UserPhoneSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()

            # generate token
            refresh = RefreshToken.for_user(user)

            # delete old verification tokens
            PhoneVerificationToken.objects.filter(user=user).delete()

            # create verification token
            rand_token = generate_sms_token()
            token = PhoneVerificationToken.objects.create(user=user, token=rand_token)
            message = send_sms(phone, f"Your OTP is {rand_token}")

            print(message.sid)

            return generate_success_response ({
                "status_code": 200,
                "detail": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            })
        else:
            return generate_error_response ({
                "status_code": 500,
                "error_type": "invalid_request",
                "detail": serializer.errors
            })
            
class SendOTPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        phone = data.get('phone')

        if not phone:
            return generate_error_response ({
                "status_code": 400,
                "error_type": "invalid_phone_number",
                "detail": {
                    "phone": [
                        "This field may not be blank."
                    ],
                }
            })
        
        if User.objects.filter(phone=phone).exists():
            return generate_error_response ({
                "status_code": 400,
                "error_type": "user_already_exists",
                "detail": {
                    "phone": [
                        "This phone is already in use."
                    ]
                }
            })
        
        # TODO: Validate phone number

        serializer = UserPhoneSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()

            # generate token
            #refresh = RefreshToken.for_user(user)

            # create verification token
            rand_token = generate_sms_token()
            token = PhoneVerificationToken.objects.create(user=user, token=rand_token)

            return generate_success_response ({
                "status_code": 200,
                "detail": "OTP sent successfully"
            })

        


class PhoneTokenObtainView(TokenObtainPairView):
    permission_classes = [AllowAny]

    serializer_class = PhoneTokenPairSerializer
            

class VerifyWithOTP(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({"message": "Hello, world!"})