# Generated by Django 2.1.7 on 2019-06-20 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='MfgType',
            field=models.CharField(choices=[('PCB', 'PCB Section'), ('FA', 'FA Section')], default='PCB', max_length=3),
        ),
    ]
