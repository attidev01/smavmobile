# Generated by Django 4.0.5 on 2022-07-01 23:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MessageStore', '0021_alter_language_battery'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='battery',
        ),
        migrations.RemoveField(
            model_name='language',
            name='battery',
        ),
    ]
