# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20150212_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='user_image_path',
            field=models.FileField(null=True, upload_to=b'  profile_pics/%Y/%m/%d'),
        ),
    ]
