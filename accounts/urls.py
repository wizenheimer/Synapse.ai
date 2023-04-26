from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"accounts", views.ProfileViewSet, basename="profile_view_set")
router.register(r"team", views.TeamViewSet, basename="team_view_set")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("register/", views.RegistrationView.as_view(), name="register"),
    path("verify-email/", views.VerifyEmail.as_view(), name="verify-email"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "password-reset-request/",
        views.PasswordResetRequest.as_view(),
        name="password-reset-request",
    ),
    path(
        "password-reset-confirm/",
        views.PasswordResetConfirm.as_view(),
        name="password-reset-confirm",
    ),
    path("", include(router.urls)),
]
