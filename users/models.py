from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from .managers import UserManager
from django.conf import settings

def sms_code_expires_in():
    return timezone.now() + settings.SMS_CODE_EXPIRY

def get_email_verification_token_expiry():
    return timezone.now() + settings.EMAIL_VERIFICATION_TOKEN_EXPIRY

# User model with Specifications:
#
# - email
# - phone
# - first_name
# - last_name
# - birth_date
# - is_active
# - is_staff
# - is_superuser
# - date_joined
# - password
# - groups
# - user_permissions
# - is_email_verified
# - is_phone_verified


class User(AbstractUser):
    id=models.AutoField(primary_key=True, editable=False, unique=True)

    phone=models.CharField(max_length=20, blank=True, null=True)
    country_code=models.CharField(max_length=20, default='+1', blank=False, null=False)
    email=models.EmailField('email address', blank=True, null=True, unique=False, default=None)
    
    birth_date=models.DateField(blank=True, null=True)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    phone_verified = models.BooleanField(default=False)
    phone_verified_at = models.DateTimeField(blank=True, null=True)

    email_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(blank=True, null=True)

    first_name=models.CharField(max_length=20, blank=True, null=True)
    last_name=models.CharField(max_length=20, blank=True, null=True)

    username=None
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

    objects=UserManager()

    def __str__(self):
        return self.email
    
class PhoneToken(models.Model):
    token = models.CharField(primary_key=True, max_length=6, blank=False, null=False)
    phone = models.CharField(max_length=20, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=sms_code_expires_in)
    attempts = models.IntegerField(default=0)

class EmailVerificationToken(models.Model):
    token = models.UUIDField(primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verification_tokens')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_email_verification_token_expiry)


# User create signal

