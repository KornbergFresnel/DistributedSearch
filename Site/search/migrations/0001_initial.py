# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-05-19 13:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Title')),
                ('summary', models.TextField(verbose_name='Summary')),
                ('url', models.CharField(max_length=225, verbose_name='URL')),
            ],
        ),
    ]
