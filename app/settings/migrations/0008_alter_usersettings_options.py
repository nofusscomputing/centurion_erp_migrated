# Generated by Django 5.1.2 on 2024-10-24 02:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0007_alter_appsettings_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usersettings',
            options={'ordering': ['user'], 'verbose_name': 'User Settings', 'verbose_name_plural': 'User Settings'},
        ),
    ]