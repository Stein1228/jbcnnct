# Generated by Django 5.1.3 on 2024-11-10 04:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0007_trabajo_habilidades'),
    ]

    operations = [
        migrations.AddField(
            model_name='trabajo',
            name='is_disponible',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='trabajo',
            name='trabajador_seleccionado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trabajos_seleccionados', to=settings.AUTH_USER_MODEL),
        ),
    ]
