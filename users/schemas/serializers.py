from rest_framework import serializers

from users.models import (
    User,
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'date_joined',
        )
        read_only_fields = fields

class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password']
        write_only_fields = ['password']

    def save(self):
        user = User(
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user