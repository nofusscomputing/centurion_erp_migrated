# Generated by Django 5.0.4 on 2024-05-13 15:30

import access.fields
import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', access.fields.AutoSlugField()),
                ('created', access.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', access.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'verbose_name_plural': 'Organizations',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.group')),
                ('team_name', models.CharField(default='', max_length=50, verbose_name='Name')),
                ('created', access.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', access.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='access.organization')),
            ],
            options={
                'verbose_name_plural': 'Teams',
                'ordering': ['team_name'],
            },
            bases=('auth.group', models.Model),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='TeamUsers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('manager', models.BooleanField(blank=True, default=False, verbose_name='manager')),
                ('created', access.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', access.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team', to='access.team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Team Users',
                'ordering': ['user'],
            },
        ),
    ]
