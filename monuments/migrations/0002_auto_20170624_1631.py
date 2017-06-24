# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-24 16:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monuments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monuments.City'),
        ),
        migrations.AddField(
            model_name='monument',
            name='address',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monuments.Address'),
        ),
        migrations.AddField(
            model_name='note',
            name='monument',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='monuments.Monument'),
        ),
        migrations.AddField(
            model_name='note',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='monuments.User'),
        ),
    ]
