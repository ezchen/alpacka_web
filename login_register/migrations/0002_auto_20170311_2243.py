# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-03-11 22:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_register', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contactmessage',
            old_name='email',
            new_name='contact_email',
        ),
        migrations.RenameField(
            model_name='contactmessage',
            old_name='message',
            new_name='contact_message',
        ),
        migrations.RenameField(
            model_name='contactmessage',
            old_name='name',
            new_name='contact_name',
        ),
    ]
