# Generated by Django 3.2.6 on 2021-09-09 03:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_formpagefieldssection_sectionformfield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sectionformfield',
            name='section',
        ),
        migrations.DeleteModel(
            name='FormPageFieldsSection',
        ),
        migrations.DeleteModel(
            name='SectionFormField',
        ),
    ]
