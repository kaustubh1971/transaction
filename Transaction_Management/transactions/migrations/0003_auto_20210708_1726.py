# Generated by Django 3.1.3 on 2021-07-08 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_auto_20210708_0546'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactionline',
            old_name='quanitity',
            new_name='quantity',
        ),
    ]
