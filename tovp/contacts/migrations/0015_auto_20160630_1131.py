# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-30 11:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0014_auto_20160413_1813'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'permissions': (('can_export', 'Can export'), ('can_delete_if_no_contributions', 'Can delete if no contributions'))},
        ),
    ]