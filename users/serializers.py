from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['id']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserEmailSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class UserPhoneSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def is_valid(self):
        # password doesn't need to be required for phone registration

        return super().is_valid()

class PhoneTokenObtainSerializer(TokenObtainPairSerializer):
    username_field = 'phone'

    class Meta:
        model = User
        fields = ['phone', 'password']

class PhoneTokenPairSerializer(PhoneTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data
    
    class Meta:
        model = User
        fields = ['phone', 'password']