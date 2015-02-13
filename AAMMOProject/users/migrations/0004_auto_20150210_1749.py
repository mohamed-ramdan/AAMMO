# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20150210_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='user_image_path',
            field=models.FileField(null=True, upload_to=b'profile_pics/%Y/%m/%d'),
            preserve_default=True,
        ),
    ]
