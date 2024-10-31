# Generated by Django 5.1.1 on 2024-10-31 00:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("agenda", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="agenda",
            name="aluno",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="aluno",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="agenda",
            name="professor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="professor",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
