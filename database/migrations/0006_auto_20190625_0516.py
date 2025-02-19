# Generated by Django 2.1.7 on 2019-06-25 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_aoistoragerecord_aoistorageserver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aoistoragerecord',
            name='AOIStorageServer',
            field=models.CharField(choices=[('AOIServer1', 'AOIServer1'), ('AOIServer', 'AOIServer'), ('AOI3DXServer', 'AOI3DXServer')], default='AOIServer1', max_length=20),
        ),
        migrations.AlterField(
            model_name='stage',
            name='Name',
            field=models.CharField(choices=[('SMT_SPI_TOP', 'SMT_SPI_TOP'), ('SMT_SPI_BOT', 'SMT_SPI_BOT'), ('SMT_AOI_TOP', 'SMT_AOI_TOP'), ('SMT_AOI_BOT', 'SMT_AOI_BOT'), ('DIP_AOI', 'DIP_AOI'), ('DIP_AOI2_IPC_RUNIN', 'DIP_AOI2_IPC_RUNIN'), ('DIP_AOI2', 'DIP_AOI2'), ('FINAL_AOI', 'FINAL_AOI'), ('FA_AOI', 'FA_AOI'), ('AXI_OFFLINE_SAMPLINE', 'AXI_OFFLINE_SAMPLINE'), ('AXI_ONLINE_DIP', 'AXI_ONLINE_DIP'),('AXI_7600SIII','AXI_7600SIII')], default='SMT_SPI_TOP', max_length=50, unique=True),
        ),
    ]
