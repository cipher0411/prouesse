# Generated by Django 5.0.6 on 2024-06-10 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_otptoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='d6acec', max_length=6),
        ),
    ]
