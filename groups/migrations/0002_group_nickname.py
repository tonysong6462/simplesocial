# Generated by Django 4.2.23 on 2025-06-17 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='nickname',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
