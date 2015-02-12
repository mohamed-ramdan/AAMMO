# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_photo',
            field=models.FileField(upload_to=b'static/uploads/article_pics/%Y/%m/%d'),
        ),
    ]
