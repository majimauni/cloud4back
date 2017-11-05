# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-04 04:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Concurso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreconcu', models.CharField(max_length=100)),
                ('imagenurl', models.CharField(max_length=100)),
                ('imagenconcu', models.ImageField(upload_to='imagen/')),
                ('urlconcu', models.CharField(max_length=100)),
                ('feini', models.DateTimeField()),
                ('fefin', models.DateTimeField()),
                ('premio', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=50)),
                ('contrasena', models.CharField(max_length=50)),
                ('_token', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechasub', models.DateTimeField()),
                ('estado', models.CharField(max_length=50)),
                ('videoSubido', models.FileField(upload_to='videosSubidos/')),
                ('videoPublicado', models.FileField(upload_to='videosPublicados/')),
                ('descrip', models.CharField(max_length=200)),
                ('nombreconcursante', models.CharField(max_length=50)),
                ('apellidoconcursante', models.CharField(max_length=50)),
                ('emailconcursante', models.EmailField(max_length=50)),
                ('particoncu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project1.Concurso')),
            ],
        ),
        migrations.AddField(
            model_name='concurso',
            name='administraconcu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project1.Usuario'),
        ),
    ]
