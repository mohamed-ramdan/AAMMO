# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20150212_1351'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_text', models.TextField()),
                ('article_id', models.ForeignKey(to='article.Article')),
                ('comment_id', models.ForeignKey(to='comments.Comment')),
                ('entity_id', models.ForeignKey(to='article.Entity')),
            ],
        ),
    ]
