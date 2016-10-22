# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-13 03:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_heading', models.CharField(max_length=200)),
                ('task_description', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('expiration_date', models.DateTimeField(verbose_name='expiration date')),
            ],
        ),
    ]
