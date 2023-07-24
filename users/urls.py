from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    HelloView, 
    CreateUserWithEmailView,
    CreateUserWithPhoneView,
    PhoneTokenObtainView,
    ProtectedView,
    VerifyWithOTPView,
    VerifyWithEmailView,
    LogoutView,
)

urlpatterns = [
    path('', HelloView.as_view(), name='index'),
    path('protected', ProtectedView.as_view(), name='protected'),

    path('token/blacklist', LogoutView.as_view(), name='user_logout'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/email', TokenObtainPairView.as_view(), name='token_obtain_pair_email'),
    path('token/phone', PhoneTokenObtainView.as_view(), name='token_obtain_pair_phone'),

    path('create/email', CreateUserWithEmailView.as_view(), name='user_create_email'),
    path('create/phone', CreateUserWithPhoneView.as_view(), name='user_create_phone'),

    path('verify/otp', VerifyWithOTPView.as_view(), name='verify_with_otp'),
    path('verify/email/<str:token>', VerifyWithEmailView.as_view(), name='verify_with_email'),
]