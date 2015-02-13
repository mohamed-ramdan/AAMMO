# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20150212_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='entity_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='entity',
            name='entity_time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]
