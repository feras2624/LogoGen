# Generated by Django 4.2.13 on 2024-05-27 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LogoGen', '0004_remove_logo_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='logo',
            name='img',
            field=models.CharField(default='', max_length=15000),
        ),
    ]
