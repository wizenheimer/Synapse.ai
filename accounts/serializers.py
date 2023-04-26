from rest_framework import serializers
from .models import User, Team
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(read_only=True, many=True)
    snippets = SnippetSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ["email", "teams", "snippets"]
