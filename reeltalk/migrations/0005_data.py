from django.db import migrations
from django.core.management import call_command


def loadfixture(apps, schema_editor):
    fixtures = 'groups people reviews shows userProfiles'.split(' ')
    call_command('loaddata', *fixtures)


class Migration(migrations.Migration):

    dependencies = [
        ('reeltalk', '0004_userprofile'),
    ]

    operations = [
        migrations.RunPython(loadfixture),
    ]
