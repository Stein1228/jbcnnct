# Generated by Django 5.1.3 on 2024-11-10 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0008_trabajo_is_disponible_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trabajo',
            name='is_completado',
            field=models.BooleanField(default=False),
        ),
    ]
