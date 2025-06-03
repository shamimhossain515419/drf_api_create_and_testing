import os

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.authapi.serializers import (
    CustomEmailTokenObtainPairSerializer,
    UpdateProfileSerializer,
)
from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Custom login view to set JWT token in HttpOnly cookie
from rest_framework.response import Response

# Logout API — cookie clear করবে
from rest_framework.views import APIView


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response()
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        response.data = {"message": "Successfully logged out"}
        return response


class MyTokenObtainPairCustomView(TokenObtainPairView):
    serializer_class = CustomEmailTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            data = response.data
            refresh = data.get("refresh")
            access = data.get("access")

            response = Response({"message": "Login successful"}, status=200)
            response.set_cookie(
                key="access_token",
                value=access,
                httponly=True,
                samesite="Lax",
                secure=False,
                max_age=int(os.getenv("ACCESS_TOKEN_LIFETIME_MINUTES")) * 60,
            )
            response.set_cookie(
                key="refresh_token",
                value=refresh,
                httponly=True,
                samesite="Lax",
                secure=False,
                max_age=int(os.getenv("REFRESH_TOKEN_LIFETIME_DAYS")) * 24 * 60 * 60,
            )
        return response


class MyTokenRefreshView(TokenRefreshView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if "refresh" not in request.data:
            refresh_token = request.COOKIES.get("refresh_token")
            if refresh_token:
                data = request.data.copy()
                data["refresh"] = refresh_token
                request._full_data = data
            else:
                return Response({"refresh": ["No refresh token provided."]}, status=400)

        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            data = response.data
            access = data.get("access")
            response = Response({"message": "Token refreshed"}, status=200)
            response.set_cookie(
                key="access_token",
                value=access,
                httponly=True,
                samesite="Lax",
                secure=False,
                max_age=int(os.getenv("ACCESS_TOKEN_LIFETIME_MINUTES", 15)) * 60,
            )
        return response


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UpdateProfileSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Profile updated successfully", "data": serializer.data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
