# Generated by Django 4.2.13 on 2024-05-27 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LogoGen', '0005_logo_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logo',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
