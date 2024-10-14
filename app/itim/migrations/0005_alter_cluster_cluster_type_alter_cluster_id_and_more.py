# Generated by Django 5.1.2 on 2024-10-13 15:27

import access.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0003_alter_organization_id_alter_organization_manager_and_more'),
        ('itim', '0004_alter_service_config_key_variable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cluster',
            name='cluster_type',
            field=models.ForeignKey(blank=True, default=None, help_text='Type of Cluster', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='itim.clustertype', verbose_name='Cluster Type'),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='id',
            field=models.AutoField(help_text='ID for this cluster', primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='is_global',
            field=models.BooleanField(default=False, help_text='Is this a global object?', verbose_name='Global Object'),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='model_notes',
            field=models.TextField(blank=True, default=None, help_text='Tid bits of information', null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='parent_cluster',
            field=models.ForeignKey(blank=True, default=None, help_text='Parent Cluster for this cluster', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='itim.cluster', verbose_name='Parent Cluster'),
        ),
        migrations.AlterField(
            model_name='clustertype',
            name='id',
            field=models.AutoField(help_text='ID for this cluster type', primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='clustertype',
            name='is_global',
            field=models.BooleanField(default=False, help_text='Is this a global object?', verbose_name='Global Object'),
        ),
        migrations.AlterField(
            model_name='clustertype',
            name='model_notes',
            field=models.TextField(blank=True, default=None, help_text='Tid bits of information', null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='clustertype',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='port',
            name='id',
            field=models.AutoField(help_text='ID of this port', primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='port',
            name='is_global',
            field=models.BooleanField(default=False, help_text='Is this a global object?', verbose_name='Global Object'),
        ),
        migrations.AlterField(
            model_name='port',
            name='model_notes',
            field=models.TextField(blank=True, default=None, help_text='Tid bits of information', null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='port',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='service',
            name='id',
            field=models.AutoField(help_text='Id for this Service', primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='service',
            name='is_global',
            field=models.BooleanField(default=False, help_text='Is this a global object?', verbose_name='Global Object'),
        ),
        migrations.AlterField(
            model_name='service',
            name='model_notes',
            field=models.TextField(blank=True, default=None, help_text='Tid bits of information', null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='service',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
    ]