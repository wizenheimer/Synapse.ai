# Generated by Django 4.2 on 2023-04-21 14:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("snippets", "0001_initial"),
        ("schema", "0001_initial"),
        ("accounts", "0003_alter_team_token"),
    ]

    operations = [
        migrations.CreateModel(
            name="SnippetAssignment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("can_view_snippet", models.BooleanField(default=True)),
                ("can_edit_snippet", models.BooleanField(default=True)),
                ("begin_date", models.DateTimeField(auto_now_add=True)),
                (
                    "snippet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="snippets.snippet",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SchemaAssignment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("can_view_schema", models.BooleanField(default=True)),
                ("can_edit_schema", models.BooleanField(default=True)),
                ("begin_date", models.DateTimeField(auto_now_add=True)),
                (
                    "schema",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="schema.schema"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
