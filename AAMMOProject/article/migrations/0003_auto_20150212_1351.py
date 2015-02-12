# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20150211_0701'),
        ('article', '0002_auto_20150211_1331'),
    ]

    operations = [
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='entity',
            name='author_id',
            field=models.ForeignKey(default=1, to='users.Users'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='likes',
            name='entity_like_id',
            field=models.ForeignKey(to='article.Entity'),
        ),
        migrations.AddField(
            model_name='likes',
            name='user_like_id',
            field=models.ForeignKey(to='users.Users'),
        ),
    ]
