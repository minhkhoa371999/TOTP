# Generated by Django 3.0.5 on 2023-04-05 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otp',
            name='start_otp',
        ),
    ]
