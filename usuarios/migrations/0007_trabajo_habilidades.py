# Generated by Django 5.1.2 on 2024-10-28 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_trabajo_postulacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='trabajo',
            name='habilidades',
            field=models.ManyToManyField(blank=True, to='usuarios.habilidades'),
        ),
    ]
