# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-03 18:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github_co', '0002_auto_20170203_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='colombian',
            field=models.BooleanField(default=False),
        ),
    ]
