# Generated by Django 5.1.2 on 2024-10-13 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itam', '0006_alter_device_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='devicemodel',
            options={'ordering': ['manufacturer', 'name'], 'verbose_name': 'Device Model', 'verbose_name_plural': 'Device Models'},
        ),
    ]
