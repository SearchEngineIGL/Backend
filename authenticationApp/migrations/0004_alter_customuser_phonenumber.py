# Generated by Django 5.0 on 2023-12-27 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticationApp', '0003_customuser_fullname_customuser_phonenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='PhoneNumber',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
