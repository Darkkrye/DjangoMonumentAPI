# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-27 12:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monuments', '0002_auto_20170625_1322'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('humidity', models.IntegerField()),
                ('temp_min', models.CharField(max_length=200)),
                ('temp_max', models.CharField(max_length=200)),
                ('visibility', models.IntegerField()),
                ('wind_speed', models.CharField(max_length=200)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monuments.City')),
            ],
        ),
    ]