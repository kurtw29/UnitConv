# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-22 04:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unit_conv_app', '0005_auto_20180822_0422'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='conversion',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feedback',
            name='feature',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feedback',
            name='layout',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feedback',
            name='other',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feedback',
            name='speed',
            field=models.BooleanField(default=False),
        ),
    ]
