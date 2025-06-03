from django.urls import path

from django.urls import path
from api.authapi.views import (
    LogoutView,
    MyTokenObtainPairCustomView,
    MyTokenRefreshView,
    RegisterView,
    UpdateProfileView,
)

urlpatterns = [
    path("registration/", RegisterView.as_view(), name="registration"),
    path("login/", MyTokenObtainPairCustomView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", MyTokenRefreshView.as_view(), name="token_refresh"),
    path("profile/update/", UpdateProfileView.as_view(), name="update_profile"),
]
