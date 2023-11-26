from django.conf import settings
from django.utils import timezone

from rest_framework.views import APIView

from core.utils.http import (
    generate_error_response,
    generate_success_response,
    validate_uuid4,
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

import asyncio

from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.cache import cache_page, never_cache
from django.utils.decorators import method_decorator

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.account.models import EmailAddress

from silk.profiling.profiler import silk_profile

from rest_framework_simplejwt.tokens import RefreshToken

from core.utils.tasks import (
    send_email,
    send_phone_code,
    call_phone_with_code,
)

from .models import (
    User,
    PhoneToken,
    EmailVerificationToken,
)

from core.utils.users import (
    generate_sms_code,
    generate_email_verification_token,
)

from .schemas.registration import (
    EmailRegistrationSchema,
    PhoneRegistrationSchema,
)

from .schemas.validation import (
    EmailLoginSchema,
    SendOTPBodySchema,
    OTPVerifyBodySchema,
    NormalizePhoneSchema,
)

from .schemas.serializers import (
    UserSerializer,
)


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://localhost:3000'
    client_class = OAuth2Client


class EmailRegisterView(APIView):
    permission_classes = [AllowAny,]
    serializer_class = EmailRegistrationSchema

    #@silk_profile(name='EmailRegisterView.post')
    #@method_decorator(cache_page(60*60*2))
    def post(self, request, *args, **kwargs):
        serializer = EmailRegistrationSchema(data=request.data)

        is_valid = serializer.is_valid()

        if not is_valid:
            return generate_error_response({
                "error_type": "invalid_request",
                "status": 400,
                "errors": serializer.errors,
            })
        
        serializer.save()

        # at this point, email should be sent to the user

        # generate email verification token

        if (settings.SEND_EMAIL_VERIFICATION):

            email_verification_token = generate_email_verification_token()

            asyncio.run(EmailVerificationToken.objects.acreate(
                token=email_verification_token,
                user=serializer.instance,
            ))
            
            send_email(
                subject='Welcome to Reservation App!',
                html_content=f'<h1>Welcome to Reservation App!</h1><p>Thank you for registering with us!</p> <p>Please verify your email by clicking <a href="{settings.VERIFY_EMAIL_URL}?token={email_verification_token}">here</a>.</p>',
                recipient_list=[serializer.instance.email,],
            )

        if serializer.instance:
            return generate_success_response({
                "detail": "User created successfully.",
                "status": 201,
            })
        
        
        return generate_error_response({
            "error_type": "invalid_request",
            "status": 400,
            "detail": "Bad email or password.",
        })
    
class EmailVerifyView(APIView):
    permission_classes = [AllowAny,]
    serializer_class = EmailLoginSchema

    @silk_profile(name='EmailVerifyView.post')
    @method_decorator(cache_page(60*60*2))
    def post(self, request, *args, **kwargs):
        serializer = EmailLoginSchema(data=request.data)
        is_valid = serializer.is_valid()

        if (not is_valid):
            return generate_error_response({
            "error_type": "invalid_request",
            "status": 400,
            "detail": "Bad email or password.",
        })
        
        # the user is authenticated at this point

        if serializer.validated_data['user']:

            refresh = RefreshToken.for_user(serializer.validated_data['user'])
            return Response({
                "detail": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        
        return generate_error_response({
            "error_type": "invalid_request",
            "status": 400,
            "detail": "Bad email or password.",
        })
    
    
class GetAllUsers(APIView):
    permission_classes = [AllowAny,]

    #@silk_profile(name='GetAllUsers.get')
    @method_decorator(cache_page(60*60*2))
    def get(self, request, *args, **kwargs):

        users = User.objects.all()
        serialized_users = UserSerializer(users, many=True)

        return generate_success_response({
            "data": serialized_users.data,
            "status": 200,
        })
    
class PhoneRegisterView(APIView):
    permission_classes = [AllowAny,]
    serializer_class = PhoneRegistrationSchema

    #@silk_profile(name='PhoneRegisterView.post')
    @method_decorator(cache_page(60*60*2))
    def post(self, request, *args, **kwargs):
        serializer = PhoneRegistrationSchema(data=request.data)

        is_valid = serializer.is_valid()

        if not is_valid:
            return generate_error_response({
                "error_type": "invalid_request",
                "status": 400,
                "detail": serializer.errors,
            })
        
        serializer.save()

        # send email verification token

        email_verification_token = generate_email_verification_token()

        asyncio.run(EmailVerificationToken.objects.acreate(
            token=email_verification_token,
            user=serializer.instance,
        ))
        
        send_email(
            subject='Welcome to Reservation App!',
            html_content=f'<h1>Welcome to Reservation App!</h1><p>Thank you for registering with us!</p> <p>Please verify your email by clicking <a href="{settings.VERIFY_EMAIL_URL}?token={email_verification_token}">here</a>.</p>',
            recipient_list=[serializer.instance.email,],
        )

        if serializer.instance:
            serializer.instance.phone_verified = True
            serializer.instance.phone_verified_at = timezone.now()

            asyncio.run(serializer.instance.asave())
            return generate_success_response({
                "detail": "User created successfully.",
                "status": 201,
            })
        
        return Response(None, status=status.HTTP_400_BAD_REQUEST)
    
class PhoneVerifyView(APIView):
    permission_classes = [AllowAny,]
    serializer_class = OTPVerifyBodySchema

    #@silk_profile(name='PhoneLoginView.post')
    @method_decorator(cache_page(60*60*2))
    def post(self, request, *args, **kwargs):
        serializer = OTPVerifyBodySchema(data=request.data)
        serializer.is_valid(raise_exception=True)

        # ensure that user exists

        user = User.objects.filter(phone=serializer.data.get('phone')).first()

        if not user:
            return generate_error_response({
                "error_type": "invalid_request",
                "status": 400,
                "detail": "User does not exist.",
            })
        
        phone_token = PhoneToken.objects.filter(
            phone=serializer.data.get('phone'),
            expires_at__gte=timezone.now(),
        ).first()

        if not phone_token:
            return generate_error_response({
                "error_type": "invalid_token",
                "status": 400,
                "detail": "The provided token is not valid!",
            })
        
        otps_match = phone_token.token == serializer.data.get('token')

        if not otps_match:
            if (phone_token.attempts + 1) >= settings.SMS_CODE_MAXIMUM_ATTEMPTS:
                phone_token.delete()

                return generate_error_response({
                    "error_type": "token_attempts_exceeded",
                    "status": 400,
                    "detail": "The provided token attempts exceeded!",
                })
            
            phone_token.attempts += 1
            phone_token.save()

            return generate_error_response({
                "error_type": "invalid_token",
                "status": 400,
                "detail": "The provided token is not valid!",
            })

        # delete all previous tokens for this phone number

        PhoneToken.objects.filter(
            phone=serializer.data.get('phone'),
        ).delete()

        refresh = RefreshToken.for_user(user)

        return generate_success_response({
            "detail": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        })
        
class EmailExistsView(APIView):
    def get(self, request, email=None):
        if not email:
            return generate_error_response({
                "error_type": "invalid_request",
                "status": 400,
                "detail": {
                    "email": "This field is required.",
                },
            })
        
        if email:
            if User.objects.filter(email=email).exists():
                return generate_success_response({
                    "detail": {
                        "exists": True,
                    }
                })
            else:
                return generate_success_response({
                    "detail": {
                        "exists": False,
                    }
                })
        else:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
    
class PhoneExistsView(APIView):
    def post(self, request):
        serializer = NormalizePhoneSchema(data=request.data)

        if not serializer.is_valid():
            return generate_error_response({
                "error_type": "invalid_request",
                "status": 400,
                "detail": serializer.errors,
            })
        
        phone = serializer.data.get('phone')

        if User.objects.filter(phone=phone).exists():
            return generate_success_response({
                "detail": {
                    "exists": True,
                }
            })
        else:
            return generate_success_response({
                "detail": {
                    "exists": False,
                }
            })
        
class SendPhoneSMSVerificationView(APIView):
    permission_classes = [AllowAny,]

    @method_decorator(cache_page(60*60*2))
    def post(self, request):
        serializer = SendOTPBodySchema(data=request.data)

        if not serializer.is_valid():
            return generate_error_response({
                "error_type": "invalid_request",
                "status": 400,
                "detail": serializer.errors,
            })
        
        code = generate_sms_code()

        # delete all previous tokens for this phone number

        asyncio.run(PhoneToken.objects.filter(
            phone=serializer.data.get('phone'),
        ).adelete())

        asyncio.run(PhoneToken.objects.acreate(
            phone=serializer.data.get('phone'),
            token=code,
        ))
        
        try:
            send_phone_code(
            phone=serializer.data.get('phone'),
            code=code,
        )
        except:
            return generate_error_response({
                "error_type": "invalid_request",
                "status": 400,
                "detail": "Invalid phone number.",
            })
       

        return generate_success_response({
            "detail": "SMS sent successfully.",
        })
    
class PhoneSMSVerifyView(APIView):
    permission_classes = [AllowAny,]

    #@silk_profile(name='PhoneSMSVerifyView.post')
    @method_decorator(cache_page(60*60*2))
    def post(self, request):
        serializer = OTPVerifyBodySchema(data=request.data)

        serializer.is_valid(raise_exception=True)
        
        phone_token = PhoneToken.objects.filter(
            phone=serializer.data.get('phone'),
            expires_at__gte=timezone.now(),
        ).first()

        if not phone_token:
            return generate_error_response({
                "error_type": "invalid_token",
                "status": 400,
                "detail": "The provided token is not valid!",
            })
        
        otps_match = phone_token.token == serializer.data.get('token')

        if not otps_match:
            if (phone_token.attempts + 1) >= settings.SMS_CODE_MAXIMUM_ATTEMPTS:
                phone_token.delete()

                return generate_error_response({
                    "error_type": "token_attempts_exceeded",
                    "status": 400,
                    "detail": "The provided token attempts exceeded!",
                })
            
            phone_token.attempts += 1
            phone_token.save()

            return generate_error_response({
                "error_type": "invalid_token",
                "status": 400,
                "detail": "The provided token is not valid!",
            })
        
        return generate_success_response({
            "detail": "SMS sent successfully.",
        })
    
class VerifyEmailView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        user = request.user
        token = request.GET.get('token')

        if user.email_verified:
            return generate_error_response({
                "error_type": "invalid_request",
                "status": 400,
                "detail": "Email is already verified.",
            })

        if not token:
            return generate_error_response({
                "error_type": "invalid_request",
                "status": 400,
                "detail": "Token is required.",
            })
        
        # verify that token is uuid

        if not validate_uuid4(token):
            return generate_error_response({
                "error_type": "invalid_token",
                "status": 400,
                "detail": "The provided token is not valid!",
            })
        
        email_verification_token = EmailVerificationToken.objects.filter(
            token=token,
            expires_at__gte=timezone.now(),
        ).first()

        if not email_verification_token:
            return generate_error_response({
                "error_type": "invalid_token",
                "status": 400,
                "detail": "The provided token is not valid!",
            })

        user.email_verified = True
        user.email_verified_at = timezone.now()

        email_address = EmailAddress.objects.filter(
            user=user,
            email=user.email,
        ).first()

        if not email_address:
            EmailAddress.objects.create(
                user=user,
                email=user.email,
                verified=True,
                primary=True,
            )
        else:
            email_address.verified = True
            email_address.save()


        asyncio.run(user.asave())
        asyncio.run(email_verification_token.adelete())

        return generate_success_response({
            "detail": "Email verified successfully.",
        })
    
class CallUserWithCodeView(APIView):
    permission_classes = [AllowAny,]

    #@silk_profile(name='CallUserWithCodeView.post')
    @method_decorator(cache_page(60*60*2))
    def post(self, request):
        serializer = SendOTPBodySchema(data=request.data)

        if not serializer.is_valid():
            return generate_error_response({
                "error_type": "invalid_request",
                "status": 400,
                "detail": serializer.errors,
            })
        
        phone = serializer.data.get('phone')

        # verify that phone is valid

        code = generate_sms_code()

        # delete all previous tokens for this phone number

        asyncio.run(PhoneToken.objects.filter(
            phone=phone,
        ).adelete())

        asyncio.run(PhoneToken.objects.acreate(
            phone=phone,
            token=code,
        ))
        
        call_phone_with_code(
            phone=phone,
            code=code,
        )

        return generate_success_response({
            "detail": "SMS sent successfully.",
        })