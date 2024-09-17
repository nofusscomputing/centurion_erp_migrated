# Generated by Django 5.0.8 on 2024-09-17 03:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0003_alter_project_external_system_projectstate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='state',
            field=models.ForeignKey(help_text='Staate of the project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='project_management.projectstate', verbose_name='Project State'),
        ),
    ]
