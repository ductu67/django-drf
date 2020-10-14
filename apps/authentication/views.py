from datetime import datetime
import jwt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.views import JSONWebTokenAPIView
import apps.utils.response_interface as rsp
from ProjectsManager.settings import SECRET_KEY, JWT_AUTH
from .custom_auth import JWTAuthentication
from .models import TokenUser
from .serializers import *


# from ..utils.views_helper import GenericViewSet


class LoginViewSet(JSONWebTokenAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        token_jwt = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + JWT_AUTH.get('JWT_EXPIRATION_DELTA'),
        }, SECRET_KEY)
        TokenUser.objects.create(token=token_jwt.decode(), user=user)

        general_response = rsp.Response(True, message="User logged in successfully", data=token_jwt).generate_response()
        return Response(general_response, status=status.HTTP_201_CREATED)


class LogoutViewSet(JSONWebTokenAPIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            TokenUser.objects.filter(user=user, token=request.auth).delete()

        general_response = rsp.Response(True, message="logout success", data=None).generate_response()
        return Response(general_response, status=status.HTTP_200_OK)
