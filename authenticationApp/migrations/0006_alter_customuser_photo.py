# Generated by Django 5.0 on 2024-01-05 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticationApp', '0005_alter_customuser_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='photo',
            field=models.ImageField(blank=True, default='/profile_pictures/profile_pictures/default.png', null=True, upload_to='profile_pictures/'),
        ),
    ]
