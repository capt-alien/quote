# Generated by Django 2.2.5 on 2019-09-23 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='updated_at',
        ),
    ]