# Generated by Django 4.0 on 2022-07-20 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_orderproduct_product_orderproduct_profile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.order', verbose_name='Pedido'),
        ),
    ]
