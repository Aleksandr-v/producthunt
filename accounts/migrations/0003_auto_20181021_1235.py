# Generated by Django 2.0.2 on 2018-10-21 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20181021_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='images/users/profiles'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[(' ', ' '), ('m', 'Male'), ('f', 'Female')], max_length=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='instagram',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='vk',
            field=models.URLField(blank=True),
        ),
    ]
