# Generated by Django 5.1.6 on 2025-02-15 15:21

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Bot",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "platform",
                    models.CharField(
                        choices=[("telegram", "Telegram")],
                        default="telegram",
                        max_length=256,
                    ),
                ),
                ("bot_token", models.CharField(max_length=256, unique=True)),
                ("webhook_secret", models.CharField(blank=True, max_length=256)),
                ("webhook_url_prefix", models.URLField(max_length=512)),
            ],
            options={
                "verbose_name": "Bot",
                "verbose_name_plural": "Bots",
                "ordering": ("-created_at",),
                "get_latest_by": "created_at",
                "abstract": False,
            },
        ),
    ]
