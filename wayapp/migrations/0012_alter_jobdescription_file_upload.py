# Generated by Django 5.0.2 on 2024-06-21 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wayapp', '0011_alter_jobdescription_employer_alter_jobpost_username_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobdescription',
            name='file_upload',
            field=models.FileField(null=True, upload_to='uploads/% Y/% m/% d/'),
        ),
    ]
