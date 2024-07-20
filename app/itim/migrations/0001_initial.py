# Generated by Django 5.0.7 on 2024-07-20 20:40

import access.fields
import access.models
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('access', '0001_initial'),
        ('itam', '0002_device_config'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClusterType',
            fields=[
                ('is_global', models.BooleanField(default=False)),
                ('model_notes', models.TextField(blank=True, default=None, null=True, verbose_name='Notes')),
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(help_text='Name of the Cluster Type', max_length=50, verbose_name='Name')),
                ('slug', access.fields.AutoSlugField()),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists])),
            ],
            options={
                'verbose_name': 'ClusterType',
                'verbose_name_plural': 'ClusterTypes',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('is_global', models.BooleanField(default=False)),
                ('model_notes', models.TextField(blank=True, default=None, null=True, verbose_name='Notes')),
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(help_text='Name of the Cluster', max_length=50, verbose_name='Name')),
                ('slug', access.fields.AutoSlugField()),
                ('config', models.JSONField(blank=True, default=None, help_text='Cluster Configuration', null=True, verbose_name='Configuration')),
                ('devices', models.ManyToManyField(blank=True, default=None, help_text='Devices that are deployed upon the cluster.', related_name='cluster_device', to='itam.device', verbose_name='Devices')),
                ('node', models.ManyToManyField(blank=True, default=None, help_text='Hosts for resource consumption that the cluster is deployed upon', related_name='cluster_node', to='itam.device', verbose_name='Nodes')),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists])),
                ('parent_cluster', models.ForeignKey(blank=True, default=None, help_text='Parent Cluster for this cluster', null=True, on_delete=django.db.models.deletion.CASCADE, to='itim.cluster', verbose_name='Parent Cluster')),
                ('cluster_type', models.ForeignKey(blank=True, default=None, help_text='Parent Cluster for this cluster', null=True, on_delete=django.db.models.deletion.CASCADE, to='itim.clustertype', verbose_name='Parent Cluster')),
            ],
            options={
                'verbose_name': 'Cluster',
                'verbose_name_plural': 'Clusters',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Port',
            fields=[
                ('is_global', models.BooleanField(default=False)),
                ('model_notes', models.TextField(blank=True, default=None, null=True, verbose_name='Notes')),
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('number', models.IntegerField(help_text='The port number', verbose_name='Port Number')),
                ('description', models.CharField(blank=True, default=None, help_text='Short description of port', max_length=80, null=True, verbose_name='Description')),
                ('protocol', models.CharField(choices=[('TCP', 'TCP'), ('UDP', 'UDP')], default='TCP', help_text='Layer 4 Network Protocol', max_length=3, verbose_name='Protocol')),
                ('created', access.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', access.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists])),
            ],
            options={
                'verbose_name': 'Protocol',
                'verbose_name_plural': 'Protocols',
                'ordering': ['number', 'protocol'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('is_global', models.BooleanField(default=False)),
                ('model_notes', models.TextField(blank=True, default=None, null=True, verbose_name='Notes')),
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(help_text='Name of the Service', max_length=50, verbose_name='Name')),
                ('config', models.JSONField(blank=True, default=None, help_text='Cluster Configuration', null=True, verbose_name='Configuration')),
                ('created', access.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', access.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('cluster', models.ForeignKey(blank=True, default=None, help_text='Cluster the service is assigned to', null=True, on_delete=django.db.models.deletion.CASCADE, to='itim.cluster', verbose_name='Cluster')),
                ('dependent_service', models.ManyToManyField(blank=True, default=None, help_text='Services that this service depends upon', to='itim.service', verbose_name='Dependent Services')),
                ('device', models.ForeignKey(blank=True, default=None, help_text='Device the service is assigned to', null=True, on_delete=django.db.models.deletion.CASCADE, to='itam.device', verbose_name='Device')),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists])),
                ('port', models.ManyToManyField(help_text='Port the service is available on', to='itim.port', verbose_name='Port')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
                'ordering': ['name'],
            },
        ),
    ]
