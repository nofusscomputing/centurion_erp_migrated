# Generated by Django 5.1.2 on 2024-11-20 02:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itam', '0018_alter_device_organization_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceoperatingsystem',
            name='device',
            field=models.ForeignKey(help_text='Device for the Operating System', on_delete=django.db.models.deletion.CASCADE, to='itam.device', unique=True, verbose_name='Device'),
        ),
    ]
