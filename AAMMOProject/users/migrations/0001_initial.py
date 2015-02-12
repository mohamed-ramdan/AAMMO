# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.IntegerField(serialize=False, primary_key=True)),
                ('user_facebook_id', models.IntegerField(unique=True)),
                ('user_name', models.CharField(max_length=100)),
                ('user_password', models.CharField(max_length=100)),
                ('user_email', models.CharField(max_length=200)),
                ('user_image_path', models.CharField(max_length=255)),
                ('user_admin_status', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
