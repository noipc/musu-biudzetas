# Generated by Django 2.2.4 on 2019-08-23 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20190816_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='pub_subsector',
            field=models.IntegerField(blank=True, choices=[(1, 'Vaikai'), (2, 'Jaunimas'), (3, 'Senjorai')], help_text='Vaikai, Jaunimas, Senjorai', null=True, verbose_name='Viešosios politikos srities kategorija'),
        ),
        migrations.AlterField(
            model_name='municipality',
            name='adult_pop',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Gyventojų skaičius nuo 15 iki 65 metų'),
        ),
        migrations.AlterField(
            model_name='municipality',
            name='area',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Savivaldybės plotas, kv. km'),
        ),
        migrations.AlterField(
            model_name='municipality',
            name='child_pop',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Gyentojų skaičius nuo 0 iki 15 metų'),
        ),
    ]