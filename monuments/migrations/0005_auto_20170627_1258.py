# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-27 12:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monuments', '0004_auto_20170627_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='weather',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='weather',
            name='main',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
