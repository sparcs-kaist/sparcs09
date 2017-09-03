# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-23 13:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_payment_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.IntegerField(choices=[(0, 'Banned'), (1, 'Pending'), (2, 'Joined'), (3, 'In Disputed'), (4, 'Paid'), (5, 'Confirmed')]),
        ),
    ]