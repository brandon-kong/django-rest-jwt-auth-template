from rest_framework.serializers import ModelSerializer
from .models import User

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
