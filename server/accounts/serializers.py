from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import User
from accounts.services import ProcessNewUserService
from utils.constants import USER_EMAIL_UNIQUE


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    phone_number = serializers.CharField(required=True, allow_null=False)
    confirm_email = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'full_name_en', 'phone_number', 'confirm_email']

    def validate_email(self, value):
        lowered_email = value.lower()
        if User.objects.filter(email=lowered_email).exists():
            raise ValidationError(USER_EMAIL_UNIQUE)
        return lowered_email

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        ProcessNewUserService(user).process()

        return user
