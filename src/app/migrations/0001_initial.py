# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-04 09:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Build',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('result', models.TextField(default='')),
            ],
            options={
                'db_table': 'builds',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('description', models.TextField(blank=True, default='')),
                ('svn_url', models.TextField()),
                ('svn_username', models.TextField(blank=True, default='')),
                ('svn_password', models.TextField(blank=True, default='')),
                ('recipient', models.TextField()),
            ],
            options={
                'db_table': 'jobs',
            },
        ),
        migrations.AddField(
            model_name='build',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='builds', to='app.Job'),
        ),
    ]
