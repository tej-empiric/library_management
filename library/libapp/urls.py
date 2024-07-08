from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("admin/staff/", StaffView.as_view(), name="staff"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("admin/staff/<int:pk>/", StaffUpdateView.as_view(), name="staff_update"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
