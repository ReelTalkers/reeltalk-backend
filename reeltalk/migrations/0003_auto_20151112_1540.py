# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reeltalk', '0002_auto_20151111_0548'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'people',
            },
        ),
        migrations.AddField(
            model_name='group',
            name='title',
            field=models.CharField(default='untitled', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='show',
            name='detail_color',
            field=models.CharField(default='#ffffff', max_length=10),
        ),
        migrations.AddField(
            model_name='show',
            name='genre',
            field=models.CharField(default='romance', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='show',
            name='background_color',
            field=models.CharField(default='#ffffff', max_length=10),
        ),
        migrations.AlterField(
            model_name='show',
            name='text_color',
            field=models.CharField(default='#000000', max_length=10),
        ),
        migrations.AddField(
            model_name='show',
            name='actors',
            field=models.ManyToManyField(related_name='portfolio', to='reeltalk.Person', blank=True),
        ),
        migrations.AddField(
            model_name='show',
            name='director',
            field=models.ForeignKey(default=1, to='reeltalk.Person'),
            preserve_default=False,
        ),
    ]
