# authapi/middleware.py

from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication


class CookieJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("access_token")
        if not token:
            return None  # No token, DRF will move to next auth class or return 401

        try:
            access_token = AccessToken(token)
            user_id = access_token["user_id"]
            user = User.objects.get(id=user_id)
            return (user, None)  # Must return a tuple of (user, auth)
        except Exception:
            raise AuthenticationFailed("Invalid or expired token")
