# Generated by Django 5.0 on 2023-12-30 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0008_rename_photo_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(upload_to='item_images/'),
        ),
    ]
