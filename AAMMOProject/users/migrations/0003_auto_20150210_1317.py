# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20150209_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='user_name',
            field=models.CharField(unique=True, max_length=100),
            preserve_default=True,
        ),
    ]
