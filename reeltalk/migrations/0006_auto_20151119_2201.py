# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('reeltalk', '0005_auto_20151117_2201'),
    ]

    operations = [
        migrations.RenameField(
            model_name='show',
            old_name='actors',
            new_name='cast',
        ),
        migrations.RemoveField(
            model_name='person',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='person',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='show',
            name='description',
        ),
        migrations.RemoveField(
            model_name='show',
            name='director',
        ),
        migrations.RemoveField(
            model_name='show',
            name='mpaa_rating',
        ),
        migrations.AddField(
            model_name='person',
            name='full_name',
            field=models.CharField(default='Some Person', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='show',
            name='awards',
            field=models.CharField(null=True, max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='show',
            name='country',
            field=models.CharField(null=True, max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='show',
            name='directors',
            field=models.ManyToManyField(to='reeltalk.Person', related_name='directions', blank=True),
        ),
        migrations.AddField(
            model_name='show',
            name='full_plot',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='show',
            name='imdb_id',
            field=models.CharField(default='0', max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='show',
            name='imdb_rating',
            field=models.DecimalField(decimal_places=1, null=True, max_digits=3, blank=True),
        ),
        migrations.AddField(
            model_name='show',
            name='imdb_votes',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='show',
            name='language',
            field=models.CharField(null=True, max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='show',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 19, 22, 0, 49, 214874, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='show',
            name='metacritic',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='show',
            name='plot',
            field=models.CharField(null=True, max_length=1000, blank=True),
        ),
        migrations.AddField(
            model_name='show',
            name='rating',
            field=models.CharField(null=True, max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='show',
            name='released',
            field=models.CharField(null=True, max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='show',
            name='type',
            field=models.CharField(default='movie', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='show',
            name='writers',
            field=models.ManyToManyField(to='reeltalk.Person', related_name='scripts', blank=True),
        ),
        migrations.AlterField(
            model_name='show',
            name='banner',
            field=models.CharField(null=True, max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='show',
            name='genre',
            field=models.CharField(null=True, max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='show',
            name='poster',
            field=models.CharField(null=True, max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='show',
            name='runtime',
            field=models.CharField(null=True, max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='show',
            name='year',
            field=models.CharField(null=True, max_length=4, blank=True),
        ),
    ]
