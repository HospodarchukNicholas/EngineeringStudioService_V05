# Generated by Django 5.0 on 2023-12-30 12:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0005_writeoff_created_by_writeoff_order_date_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='item_photos/'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='created_by',
            field=models.ForeignKey(help_text='Це поле автоматично обирає активного користувача. При потребі можна обрати іншу відповідальну особу.', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='writeoffitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1, help_text='Обираємо кількість компонентів для списання з конкретного місця. Якщо кількість буде перевищувати доступну - буде викликано exeption, щоб запобігти некоректній операції'),
        ),
    ]
