# Generated by Django 5.0 on 2023-12-30 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0006_item_photo_alter_shoppingcart_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='item_images/'),
        ),
    ]
