# Generated by Django 3.2.16 on 2022-11-27 03:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20221127_0056'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
