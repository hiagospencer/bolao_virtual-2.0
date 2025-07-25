# Generated by Django 5.2 on 2025-07-14 23:58

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("usuarios", "0014_alter_convite_codigo"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="convite",
            name="convidador",
        ),
        migrations.RemoveField(
            model_name="convite",
            name="data_envio",
        ),
        migrations.AlterField(
            model_name="convite",
            name="data_aceito",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name="CodigoConvite",
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
                ("codigo", models.UUIDField(default=uuid.uuid4, unique=True)),
                (
                    "usuario",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="convite",
            name="codigo",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="usos",
                to="usuarios.codigoconvite",
            ),
        ),
    ]
