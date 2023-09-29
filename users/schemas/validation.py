from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from users.models import (
    User,
)

from core.utils.users import (
    normalize_phone_number,
    phone_number_is_valid,
)

class EmailLoginSchema(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_null=False)
    password = serializers.CharField(required=True, allow_null=False, write_only=True)

    def validate(self, data):
        # optimized for speed

        # make sure email is unique

        if not data['email']:
            raise serializers.ValidationError({
                'email': _('Email is required.'),
            })
        
        user = User.objects.filter(email=data['email']).first()

        if not user:
            raise serializers.ValidationError({
                'email': _('Bad email or password.'),
            })

        if not user.check_password(data['password']):
            raise serializers.ValidationError({
                'password': _('Bad email or password.'),
            })

        data['user'] = user

        return data

class SendOTPBodySchema(serializers.Serializer):
    phone = serializers.CharField(required=True, allow_null=False)

    def validate(self, data):
        # make sure phone is valid

        if not data['phone']:
            raise serializers.ValidationError({
                'phone': _('Phone is required.'),
            })
        
        is_valid = phone_number_is_valid(data['phone'])

        if not is_valid[0]:
            raise serializers.ValidationError({
                'phone': _('Phone is invalid.'),
            })
        
        data['phone'] = normalize_phone_number(is_valid[1])
        
        return data
    
class OTPVerifyBodySchema(serializers.Serializer):
    phone = serializers.CharField(required=True, allow_null=False)
    token = serializers.CharField(required=True, allow_null=False)

    def validate(self, data):
        # make sure phone is valid

        if not data['phone']:
            raise serializers.ValidationError({
                'phone': _('Phone is required.'),
            })
        
        if not data['token']:
            raise serializers.ValidationError({
                'token': _('Token is required.'),
            })
        
        is_valid = phone_number_is_valid(data['phone'])

        if not is_valid[0]:
            raise serializers.ValidationError({
                'phone': _('Phone is invalid.'),
            })
        
        data['phone'] = normalize_phone_number(is_valid[1])
        
        return data
    
class NormalizePhoneSchema(serializers.Serializer):
    phone = serializers.CharField(required=True, allow_null=False)

    def validate(self, data):
        # make sure phone is valid

        if not data['phone']:
            raise serializers.ValidationError({
                'phone': _('Phone is required.'),
            })
        
        data['phone'] = normalize_phone_number(data['phone'])
        
        return data