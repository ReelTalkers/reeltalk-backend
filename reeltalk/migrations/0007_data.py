from django.db import migrations
from django.core.management import call_command


def loadfixture(apps, schema_editor):
    fixtures = 'groups people reviews shows userProfiles curatedLists'.split(' ')
    call_command('loaddata', *fixtures)


class Migration(migrations.Migration):

    dependencies = [
        ('reeltalk', '0006_auto_20151119_2201'),
    ]

    operations = [
        migrations.RunPython(loadfixture),
    ]
