# Generated by Django 4.0.10 on 2023-04-23 07:47

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_standardpage_testing_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='standardpage',
            name='draftail_content',
            field=wagtail.fields.RichTextField(blank=True, null=True),
        ),
    ]
