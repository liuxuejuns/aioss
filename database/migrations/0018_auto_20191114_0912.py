# Generated by Django 2.1.7 on 2019-11-14 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0017_auto_20190918_0248'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComponentCoordinatesFile',
            fields=[
                ('ComponentCoordinatesFileID', models.AutoField(primary_key=True, serialize=False)),
                ('SerialNumber', models.CharField(blank=True, max_length=250, null=True)),
                ('Path', models.CharField(max_length=512)),
            ],
            options={
                'db_table': 'ComponentCoordinatesFile',
            },
        ),
        migrations.AddField(
            model_name='aoistoragerecord',
            name='IsSubgraph',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='aoistoragerecord',
            name='PartNumber',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='aoistoragerecord',
            name='CreateTime',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='aoistoragerecord',
            name='FileType',
            field=models.CharField(db_index=True, max_length=1),
        ),
        migrations.AlterField(
            model_name='aoistoragerecord',
            name='LineName',
            field=models.CharField(db_index=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='aoistoragerecord',
            name='ModelName',
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='aoistoragerecord',
            name='SerialNumber',
            field=models.CharField(blank=True, db_index=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='aoistoragerecord',
            name='StageName',
            field=models.CharField(db_index=True, max_length=50),
        ),
    ]
