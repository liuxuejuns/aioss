# Generated by Django 2.1.7 on 2020-03-25 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0020_computer_ostype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='computer',
            old_name='OsType',
            new_name='OSType',
        ),
    ]
