from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from .managers import UserManager

class User(AbstractUser):
    id=models.AutoField(primary_key=True, editable=False, unique=True)

    email=models.EmailField('email address', blank=True, null=True)
    username=None
    phone=models.CharField(max_length=20, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    phone_verified = models.BooleanField(default=False)
    phone_verified_at = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

    objects=UserManager()

    def __str__(self) -> str:
        return super().__str__() or str(self.id)


class PhoneVerificationToken(models.Model):
    token = models.CharField(max_length=6, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now() + timezone.timedelta(minutes=5))