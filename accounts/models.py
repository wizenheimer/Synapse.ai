from django.db import models
from django.contrib.auth.models import AbstractUser
from random import choice
from string import ascii_uppercase

from .managers import UserManager
from schema.models import Schema
from snippets.models import Snippet


class Team(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    # token for creating invites
    token = models.CharField(max_length=255, db_index=True, null=True, blank=True)

    def update_token(self):
        # update token for the given model
        self.token = "".join(choice(ascii_uppercase) for i in range(16))
        return self.token

    def save(self, *args, **kwargs):
        # create a new token
        token = self.update_token()
        super(Team, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, db_index=True)
    # has verified email address
    is_verified = models.BooleanField(default=False)
    # has an active account
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # team
    teams = models.ManyToManyField(Team, through="TeamAssignment")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.email)


class TeamAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    # permissions
    can_add_teammate = models.BooleanField(default=True)
    can_remove_teammate = models.BooleanField(default=True)
    # join date
    begin_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"team:{str(self.team.id)} user:{str(self.user.id)}"


class SnippetAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE)
    # permissions
    can_view_snippet = models.BooleanField(default=True)
    can_edit_snippet = models.BooleanField(default=True)
    # join date
    begin_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"snippet:{str(self.snippet.id)} user:{str(self.user.id)}"


class SchemaAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    # permissions
    can_view_schema = models.BooleanField(default=True)
    can_edit_schema = models.BooleanField(default=True)
    # join date
    begin_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"snippet:{str(self.schema.id)} user:{str(self.user.id)}"
