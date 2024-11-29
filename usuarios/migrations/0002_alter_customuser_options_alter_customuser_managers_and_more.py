# Generated by Django 5.1.2 on 2024-10-24 12:54

import django.core.validators
import django.db.models.deletion
import usuarios.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={},
        ),
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='fecha_nacimiento',
            field=models.DateField(validators=[usuarios.models.validar_fecha_nacimiento]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='foto_perfil',
            field=models.ImageField(blank=True, null=True, upload_to='perfiles/'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='genero',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], max_length=1),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='nacionalidad',
            field=models.CharField(choices=[('CL', 'Chilena'), ('AR', 'Argentina'), ('BR', 'Brasileña'), ('VE', 'Venezolana'), ('PE', 'Peruana'), ('CO', 'Colombiana')], max_length=15),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='numero_telefono',
            field=models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{9,15}$', message='El número debe estar en el formato: +999999999')]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='rut',
            field=models.CharField(max_length=12),
        ),
        migrations.CreateModel(
            name='Reseña',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.TextField(max_length=500)),
                ('calificacion', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('usuario_revisado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reseñas_recibidas', to=settings.AUTH_USER_MODEL)),
                ('usuario_revisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reseñas_realizadas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ImagenReseña',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='reseñas/')),
                ('reseña', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='usuarios.reseña')),
            ],
        ),
    ]