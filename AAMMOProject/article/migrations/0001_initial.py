# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('article_title', models.CharField(max_length=300)),
                ('article_body', models.TextField()),
                ('article_photo', models.CharField(max_length=200)),
                ('article_published', models.IntegerField(default=0)),
                ('article_tag', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('no_of_likes', models.IntegerField(default=0)),
                ('entity_date', models.DateField()),
                ('entity_time', models.TimeField()),
                ('entity_type', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='entity_id',
            field=models.ForeignKey(to='article.Entity'),
        ),
    ]
