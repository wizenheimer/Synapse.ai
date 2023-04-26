from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from random import choice
from string import ascii_uppercase

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
