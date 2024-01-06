# Generated by Django 4.2.7 on 2023-11-23 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0002_shoppingcartitem_integrated'),
    ]

    operations = [
        migrations.CreateModel(
            name='WriteOff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='WriteOffItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='write_off_items', to='warehouse.writeoff')),
                ('item_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='write_off_items', to='warehouse.itemlocation')),
            ],
        ),
    ]
