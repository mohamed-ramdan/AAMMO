# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20150211_0701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='user_email',
            field=models.EmailField(unique=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='users',
            name='user_facebook_id',
            field=models.CharField(max_length=255, unique=True, null=True),
            preserve_default=True,
        ),
    ]
