from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from users.models import (
    User,
)

from core.utils.users import (
    normalize_phone_number,
)

class EmailRegistrationSchema(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_null=False)
    password = serializers.CharField(required=True, allow_null=False, write_only=True)
    first_name = serializers.CharField(required=True, allow_null=False)
    last_name = serializers.CharField(required=True, allow_null=False)

    def validate(self, data):
        # optimized for speed

        # make sure email is unique

        if not data['email']:
            self.errors['email'] = _('Email is required.')
            raise serializers.ValidationError({
                'email': _('Email is required.'),
            })
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({
                'email': _('Email already exists.'), 
            })

        return data
    
    def create(self, validated_data):
        # optimized for speed

        # make sure email is unique

        if not validated_data['email']:
            raise serializers.ValidationError({
                'email': _('Email is required.'),
            })

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )

        return user
        
class PhoneRegistrationSchema(serializers.Serializer):
    phone = serializers.CharField(required=True, allow_null=False)
    email = serializers.EmailField(required=True, allow_null=False)
    first_name = serializers.CharField(required=True, allow_null=False)
    last_name = serializers.CharField(required=True, allow_null=False)
    token = serializers.CharField(required=True, allow_null=False)

    def validate(self, data):
        # optimized for speed

        # make sure phone is unique

        if not data['phone']:
            raise serializers.ValidationError({
                'phone': _('Phone is required.'),
            })
        
        if not data['email']:
            raise serializers.ValidationError({
                'email': _('Email is required.'),
            })
        
        # normalize phone number

        data['phone'] = normalize_phone_number(data['phone'])

        if User.objects.filter(phone=data['phone']).exists():
            raise serializers.ValidationError({
                'phone': _('Phone already exists.'),
            })
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({
                'email': _('Email already exists.'),
            })

        return data
    
    def create(self, validated_data):
        # optimized for speed


        # make sure phone is unique
        

        if not validated_data['phone']:
            raise serializers.ValidationError({
                'phone': _('Phone is required.'),
            })
        
        # normalize phone number

        validated_data['phone'] = normalize_phone_number(validated_data['phone'])

        if User.objects.filter(phone=validated_data['phone']).exists():
            raise serializers.ValidationError({
                'phone': _('Phone already exists.'),
            })

        user = User.objects.create_user(
            phone=validated_data['phone'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        return user
        