from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from apps.utils.error_code import ErrorCode


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True)

    def validate(self, data):
        username = data.get('email', "")
        password = data.get('password', "")

        if not username or not password:
            raise serializers.ValidationError('password and username field required')
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed(ErrorCode.wrong_email_pass.value)
        return user
