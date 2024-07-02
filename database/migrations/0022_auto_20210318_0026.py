# Generated by Django 2.1.7 on 2021-03-18 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0021_auto_20200325_0606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='Name',
            field=models.CharField(choices=[('SMT_SPI_TOP', 'SMT_SPI_TOP'), ('SMT_SPI_BOT', 'SMT_SPI_BOT'), ('SMT_AOI_II_TOP', 'SMT_AOI_II_TOP'), ('SMT_AOI_II_BOT', 'SMT_AOI_II_BOT'), ('SMT_AOI_III_TOP', 'SMT_AOI_III_TOP'), ('SMT_AOI_III_BOT', 'SMT_AOI_III_BOT'), ('DIP_AOI', 'DIP_AOI'), ('DIP_AOI2', 'DIP_AOI2'), ('DIP_FINAL_AOI2', 'DIP_FINAL_AOI2'), ('DIP_FINAL_AOI', 'DIP_FINAL_AOI'), ('FA_AOI', 'FA_AOI'), ('AXI_5DX', 'AXI_5DX'), ('AXI_7600SII', 'AXI_7600SII'), ('AXI_7600SIII', 'AXI_7600SIII')], max_length=50, unique=True),
        ),
    ]
