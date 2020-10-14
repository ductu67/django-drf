import jwt
from jwt import ExpiredSignatureError, DecodeError
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from ProjectsManager.settings import SECRET_KEY
from apps.authentication.models import Users, TokenUser
from apps.utils.error_code import ErrorCode


class JWTAuthentication(BaseAuthentication):
    keyword = 'jwt'

    def authenticate(self, request):

        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            raise AuthenticationFailed(ErrorCode.token_empty.value)
        if len(auth) == 1:
            raise AuthenticationFailed(ErrorCode.invalid_credential.value)
        elif len(auth) > 2:
            raise AuthenticationFailed(ErrorCode.invalid_format_token.value)

        try:
            token = auth[1].decode()
        except UnicodeError:
            raise AuthenticationFailed(ErrorCode.invalid_character_token.value)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY)
        except ExpiredSignatureError:
            raise AuthenticationFailed(ErrorCode.token_expired.value)
        except DecodeError:
            raise AuthenticationFailed(ErrorCode.invalid_token.value)
        except Exception:
            raise AuthenticationFailed(ErrorCode.exception_token.value)

        try:
            user = Users.objects.get(pk=payload.get('user_id'))
        except Users.DoesNotExist:
            raise AuthenticationFailed(ErrorCode.not_found_token.value)

        if not TokenUser.objects.filter(token=token, user=user).first():
            raise AuthenticationFailed(ErrorCode.invalid_token.value)

        return user, token
