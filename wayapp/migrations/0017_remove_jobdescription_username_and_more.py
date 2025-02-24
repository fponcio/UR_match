# Generated by Django 5.0.2 on 2025-01-10 02:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wayapp', '0016_alter_jobdescription_username'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobdescription',
            name='username',
        ),
        migrations.AddField(
            model_name='jobdescription',
            name='user_name',
            field=models.OneToOneField(default='0', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='username',
            field=models.OneToOneField(default='0', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
