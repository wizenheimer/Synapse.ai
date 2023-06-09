# Generated by Django 4.2 on 2023-04-21 15:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("schema", "0001_initial"),
        ("snippets", "0001_initial"),
        (
            "accounts",
            "0005_secret_user_schemas_user_snippets_secretassignment_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="schemas",
            field=models.ManyToManyField(
                related_name="users",
                through="accounts.SchemaAssignment",
                to="schema.schema",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="secrets",
            field=models.ManyToManyField(
                related_name="users",
                through="accounts.SecretAssignment",
                to="accounts.secret",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="snippets",
            field=models.ManyToManyField(
                related_name="users",
                through="accounts.SnippetAssignment",
                to="snippets.snippet",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="teams",
            field=models.ManyToManyField(
                related_name="users",
                through="accounts.TeamAssignment",
                to="accounts.team",
            ),
        ),
    ]
