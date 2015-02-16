# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_auto_20150213_0618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_photo',
            field=models.FileField(upload_to=b'article_pics/%Y/%m/%d'),
            preserve_default=True,
        ),
    ]
