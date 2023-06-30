# Generated by Django 3.2.15 on 2023-03-25 02:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество')),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='цена товара')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='foodcartapp.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selected_products', to='foodcartapp.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'элемент заказа',
                'verbose_name_plural': 'Элементы заказа',
            },
        ),
        migrations.DeleteModel(
            name='ProductOrder',
        ),
    ]
