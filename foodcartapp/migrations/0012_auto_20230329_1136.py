# Generated by Django 3.2.15 on 2023-03-29 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0011_auto_20230329_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='called_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Подтверждено'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivered_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Доставлено'),
        ),
    ]
