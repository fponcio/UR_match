# Generated by Django 5.0.2 on 2025-01-30 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wayapp', '0029_jobdescription_contact_person_jobpost_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobdescription',
            name='contact_person',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='first_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='last_name',
            field=models.CharField(max_length=200),
        ),
    ]
