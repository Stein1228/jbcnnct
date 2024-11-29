# Generated by Django 5.1.2 on 2024-10-24 13:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_region_comuna'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='comuna',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='usuarios.comuna'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='usuarios.region'),
        ),
    ]