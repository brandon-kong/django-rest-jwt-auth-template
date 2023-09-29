from django.urls import path

from .api import (
    EmailRegisterView,
    EmailVerifyView,
    PhoneRegisterView,
    PhoneVerifyView,

    GoogleLoginView,

    EmailExistsView,
    PhoneExistsView,

    SendPhoneSMSVerificationView,
    CallUserWithCodeView,
    PhoneSMSVerifyView,

    VerifyEmailView,

    # Benchmark routes
    GetAllUsers,
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register/email/', EmailRegisterView.as_view(), name='user_create_email'),
    path('register/phone/', PhoneRegisterView.as_view(), name='user_create_phone'),
    
    path('verify/oauth/google/', GoogleLoginView.as_view(), name='google_login'),
    
    path('verify/email/', EmailVerifyView.as_view(), name='user_verify_email'),
    path('verify/phone/', PhoneVerifyView.as_view(), name='user_verify_phone'),
    
    path('otp/call/', CallUserWithCodeView.as_view(), name='user_call_phone_otp'),
    path('otp/send/', SendPhoneSMSVerificationView.as_view(), name='user_send_phone_otp'),
    path('otp/verify/', PhoneSMSVerifyView.as_view(), name='user_verify_phone_otp'),
    
    path('email/verify/', VerifyEmailView.as_view(), name='user_verify_email_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('exists/phone/', PhoneExistsView.as_view(), name='user_exists_phone'),
    path('exists/email/<str:email>', EmailExistsView.as_view(), name='user_exists_email'),

    # Benchmark routes
    path('users/', GetAllUsers.as_view(), name='get_all_users'),
]