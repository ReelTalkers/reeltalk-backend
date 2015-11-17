# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reeltalk', '0004_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='CuratedList',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('is_private', models.BooleanField(default=False)),
                ('followers', models.ManyToManyField(to='reeltalk.UserProfile', related_name='subscribed_lists', blank=True)),
                ('owner', models.ForeignKey(to='reeltalk.UserProfile')),
                ('shows', models.ManyToManyField(to='reeltalk.Show', related_name='curated_lists', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(to='reeltalk.UserProfile', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='group',
            name='users',
            field=models.ManyToManyField(to='reeltalk.UserProfile', related_name='friend_groups', blank=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(to='reeltalk.UserProfile'),
        ),
        migrations.AlterUniqueTogether(
            name='group',
            unique_together=set([('title', 'owner')]),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set([('show', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='curatedlist',
            unique_together=set([('title', 'owner')]),
        ),
    ]
