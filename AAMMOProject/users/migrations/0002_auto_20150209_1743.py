# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='user_email',
            field=models.EmailField(max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='users',
            name='user_facebook_id',
            field=models.IntegerField(unique=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='users',
            name='user_id',
            field=models.AutoField(serialize=False, primary_key=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='users',
            name='user_image_path',
            field=models.FileField(upload_to=b'profile_pics/%Y/%m/%d'),
            preserve_default=True,
        ),
    ]
