# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-29 20:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unit_conv_app', '0012_auto_20180829_1919'),
    ]

    operations = [
        migrations.DeleteModel(
            name='File',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='image_name',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='image',
            name='uploader',
        ),
        migrations.AddField(
            model_name='image',
            name='adder',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='added_image_urls', to='unit_conv_app.User'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='image',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
