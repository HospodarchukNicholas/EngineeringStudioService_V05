# Generated by Django 5.0 on 2024-01-07 16:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0018_alter_shoppingcartitem_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemlocation',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_locations', to='warehouse.item'),
        ),
    ]
