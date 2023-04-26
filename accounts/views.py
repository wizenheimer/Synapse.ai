from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
    GenericAPIView,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from random import choice
from string import ascii_uppercase
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import (
    force_str,
    smart_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import ValidationError
import jwt
from .serializers import (
    ProfileSerializer,
    RegisterSerializer,
    LoginSerializer,
    PasswordResetSerializer,
    GeneratePasswordResetToken,
)

from .models import User, Team
from .serializers import ProfileSerializer, TeamSerializer


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer

    @action(detail=False, methods=["get"])
    def me(self, request):
        user = self.request.user
        if not user.is_authenticated:
            return Response({"error": "User is not authenticated."})
        serializer = ProfileSerializer(user)
        return Response(serializer.data)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    @action(detail=True, methods=["get"])
    def get_token(self, request, pk=None):
        team = Team.objects.get(pk=pk)
        return Response({"token": team.token})

    @action(detail=True, methods=["get"])
    def reset_token(self, request, pk=None):
        team = Team.objects.get(pk=pk)
        team.token = "".join(choice(ascii_uppercase) for i in range(16))
        team.save()
        return Response({"token": team.token})


class RegistrationView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data["email"])
        # token = RefreshToken.for_user(user)
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user=user)

        current_site = get_current_site(request).domain
        relativeLink = reverse("verify-email")

        absurl = (
            "http://" + current_site + relativeLink + f"?token={token}&uidb64={uidb64}"
        )

        send_mail(
            subject="Verify email",
            message=f"Get Started:{absurl}",
            from_email="djangomailer@mail.com",
            recipient_list=[
                user.email,
            ],
        )

        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyEmail(APIView):
    def get(self, request, *args, **kwargs):
        token = request.GET.get("token")
        uidb64 = request.GET.get("uidb64")
        uid = smart_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, id=uid)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise ValidationError("Token is invalid.")
        user.is_verified = True
        user.is_active = True
        user.save()

        return Response(
            {"email": "email successfully activated."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirm(GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.data)
        uidb64 = serializer.data.get("uidb64")
        password = serializer.data.get("password")

        uid = smart_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
        user.is_active = True
        user.set_password(password)
        user.save()

        return Response({"message": "Password changed successfully."})


class PasswordResetRequest(GenericAPIView):
    serializer_class = GeneratePasswordResetToken

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        print(email)
        user = User.objects.get(email=email)
        user.is_active = False
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user=user)

        current_site = get_current_site(request).domain
        relativeLink = reverse("password-reset-confirm")

        absurl = (
            "http://" + current_site + relativeLink + f"?uidb64={uidb64}&token={token}/"
        )

        send_mail(
            subject="Verify email",
            message=f"Link:{absurl}",
            from_email="djangomailer@mail.com",
            recipient_list=[
                user.email,
            ],
        )

        return Response({"message": "Password reset request sent successfully."})
