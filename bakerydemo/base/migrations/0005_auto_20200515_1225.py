# Generated by Django 3.0.5 on 2020-05-15 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20180522_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='job_title',
            field=models.CharField(blank=True, max_length=254, null=True, verbose_name='Job title'),
        ),
    ]
