# Generated by Django 4.2.5 on 2023-10-29 13:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_event_eventstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genericuser',
            name='nric',
            field=models.CharField(max_length=9, validators=[django.core.validators.RegexValidator(message='NRIC must start with an alphabet character, followed by 8 digits, and ending with an alphabet character.', regex='^[A-Za-z]\\d{7}[A-Za-z]$'), django.core.validators.MinLengthValidator(9)]),
        ),
        migrations.AlterField(
            model_name='genericuser',
            name='phoneNum',
            field=models.CharField(max_length=8, validators=[django.core.validators.MinLengthValidator(8), django.core.validators.RegexValidator(message='Phone number entered is invalid', regex='^[89]\\d{7}$')]),
        ),
    ]