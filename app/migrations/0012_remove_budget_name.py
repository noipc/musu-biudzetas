# Generated by Django 2.2.3 on 2019-07-27 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20190723_2352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budget',
            name='name',
        ),
    ]
