# Generated by Django 4.2 on 2023-04-21 14:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_team_teamassignment_user_teams"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="token",
            field=models.CharField(
                blank=True, db_index=True, max_length=255, null=True
            ),
        ),
    ]
