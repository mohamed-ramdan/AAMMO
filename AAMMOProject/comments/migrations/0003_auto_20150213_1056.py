# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_auto_20150213_0618'),
        ('comments', '0002_auto_20150213_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_id',
            field=models.ForeignKey(related_name='away_set', default=1, to='article.Entity'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='entity_id',
            field=models.ForeignKey(related_name='home_set', to='article.Entity'),
        ),
    ]
