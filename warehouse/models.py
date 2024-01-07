from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from .modules.quantity_operations import *
from .modules.constants import *
from .modules.populate_db import *
from .modules.model_methods import *


class ItemCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    """
    A ForeignKey relationship to the same model, creating a hierarchical or recursive structure.
    The 'self' argument indicates a self-referential relationship, allowing each instance to have a parent,
    forming a tree-like structure. The relationship is nullable and blank, allowing for instances with no parent.
    """
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Owner(models.Model):
    """
    Class Owner contain information about owner of something (item etc.)
    """
    name = models.CharField(max_length=255, blank=False, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    """
    Physical or abstract location of Item (warehouse room, assembly of prototype etc.)
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    """
    A ForeignKey relationship to the same model, creating a hierarchical or recursive structure.
    The 'self' argument indicates a self-referential relationship, allowing each instance to have a parent,
    forming a tree-like structure. The relationship is nullable and blank, allowing for instances with no parent.
    """
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    """
    Class Supplier contain information about supplier of something (item etc.)
    """
    name = models.CharField(max_length=255, blank=False)
    link = models.URLField(blank=True)

    def normalize_name(self):
        """
        Зберігаємо тільки Upper щоб уникнути дублювання даних. Поки не працює, тому що коли створюємо
        новий запис "бублик", django не проводить валідацію на перевірку, чи існує "БУБЛИК", бо шукає саме "бублик"
        """
        self.name = self.name.lower()

    def save(self, *args, **kwargs):
        self.normalize_name()
        super(Supplier, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class AttributeName(models.Model):
    """
    Model representing the name of an attribute.
    - 'name': A CharField storing the attribute name, with a maximum length of 255 characters.
    It is required (blank=False) and must be unique across instances of AttributeName.
    """

    name = models.CharField(max_length=255, blank=False, unique=True)

    def __str__(self):
        return self.name


class Attribute(models.Model):
    """
    Model representing an attribute with a name-value pair.

    - 'name': A ForeignKey relationship to AttributeName, creating a link to the name of the attribute.
    - 'value': A CharField storing the value associated with the attribute, with a maximum length of 255 characters.
    """

    name = models.ForeignKey(AttributeName, on_delete=models.CASCADE, blank=False)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}: {self.value}'


class Item(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(ItemCategory, on_delete=models.SET_NULL, blank=True, null=True)
    attributes = models.ManyToManyField(Attribute, blank=True)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class ItemLocation(models.Model):
    # warehouse_flow = models.ForeignKey(WarehouseFlow, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(blank=False, default=0)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, blank=True)

    class Meta:
        unique_together = (('item', 'location', 'owner',),)

    def get_total_quantity(item):
        # метод get_total_quantity дозволяє отримати кількість всіх Item в одному місці
        return ItemLocation.objects.filter(item=item).aggregate(Sum('quantity'))['quantity__sum']

    def __str__(self):
        return f'Назва: {self.item}, Розташування: {self.location}, Кількість: {self.quantity}, Власник: {self.owner}'


class ShoppingCart(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        # ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        # ('processed', 'Processed'),
        # ('shipped', 'Shipped'),
        ('completed', 'Completed'),
    ]

    purpose = models.CharField(max_length=255, help_text='Необхідно коротко описати призначення '
                                                         'даного замовлення.'
                               )
    order_date = models.DateField(auto_now_add=True, blank=True)
    order_time = models.TimeField(auto_now_add=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft',
                              help_text='Статус впливає як будуть оброблятись дані. Draft: це як шаблон, '
                                        'програма створює записи для кожного компоненти та саму '
                                        'корзину. Approved: замовлення сформовано але ще на етапі оформлення.'
                                        ' Completed: всі компоненти доставленні, програма генерує для них записи,'
                                        ' які відповідають реальному місцезнашодженню та кількості')
    google_sheet_link = models.URLField(blank=True, max_length=255,
                                        help_text='Якщо добавити посилання - програма спробує автоматично згенерувати всі компоненти та добавити в корзину')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                   help_text='Це поле автоматично обирає активного користувача. При потребі можна обрати іншу відповідальну особу.')

    def save(self, *args, **kwargs):
        super(ShoppingCart, self).save(*args, **kwargs)
        # обовязвоко оновлюємо всі cart_items щоб в їх def save виконались необхідні операції
        for cart_item in self.cart_items.all():
            cart_item.save()

    def __str__(self):
        return f'Замовлення №{self.id}: {self.purpose}. Статус: {self.status}'


class ShoppingCartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='cart_items')
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ItemCategory, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(blank=False, default=1)
    product_link = models.URLField(blank=True)
    supplier = models.ForeignKey(Supplier, null=True, on_delete=models.CASCADE, blank=True)
    brand = models.CharField(max_length=255, blank=True)
    item_number = models.CharField(max_length=255, blank=True)
    note = models.CharField(max_length=255, blank=True)
    invoice_link = models.URLField(blank=True)
    storage_place = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, blank=True, null=True)
    integrated = models.BooleanField(default=False,
                                     editable=False)  # дозволяє відслідкувати чи вже було інтегровано в систему, тобто якщо батьківстьке замовлення було виконане

    def save(self, *args, **kwargs):
        super(ShoppingCartItem, self).save(*args, **kwargs)
        if self.cart.status == 'completed' and not self.integrated:
            # якщо ShoppingCartItem вже було інтегровано в систему, повторно це не робимо
            self.create_item_location()
            ShoppingCartItem.objects.filter(pk=self.pk).update(integrated=True)

    def create_item_location(self):
        item, item_created = Item.objects.get_or_create(name=self.name, category=self.category)
        if not self.owner:
            owner, owner_created = Owner.objects.get_or_create(name=DEFAULT_COMPANY_NAME)
        else:
            owner = self.owner
        if not self.storage_place:
            location, location_created = Location.objects.update_or_create(name=DEFAULT_LOCATION)
        else:
            location = self.storage_place

        item_location, item_location_created = ItemLocation.objects.get_or_create(
            item=item,
            owner=owner,
            location=location,
            defaults={'quantity': 0}
        )

        income_quantity = self.quantity
        if item_location_created:
            item_location.quantity = income_quantity
            item_location.save()
        elif not item_location_created:
            QuantityManager.add_quantity(item_location, income_quantity)
            # добавляємо якщо запис вже існує

            # quantity += item_location.quantity
            # item_location.quantity = quantity
            # item_location.save()



    def __str__(self):
        return self.name

    # class Meta:
    #     unique_together = (('cart', 'name',),)


class WriteOff(models.Model):
    reason = models.CharField(max_length=255, help_text=HELP_TEXT_WriteOff_reason)
    order_date = models.DateField(auto_now_add=True, blank=True, null=True)
    order_time = models.TimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        super(WriteOff, self).save(*args, **kwargs)
        # обовязвоко оновлюємо всі cart_items щоб в їх def save виконались необхідні операції
        for write_off_item in self.write_off_items.all():
            write_off_item.save()

    def __str__(self):
        return self.reason


class WriteOffItem(models.Model):
    write_off = models.ForeignKey(WriteOff, on_delete=models.CASCADE, related_name='write_off_items', )
    item_location = models.ForeignKey(ItemLocation, on_delete=models.CASCADE, related_name='write_off_items',
                                      help_text=HELP_TEXT_WriteOffItem_item_location)
    quantity = models.PositiveIntegerField(blank=False, default=1,
                                           help_text=HELP_TEXT_WriteOffItem_quantity)

    def clean(self):
        # Check if the quantity in WriteOffItem exceeds the available quantity in ItemLocation
        if self.quantity > self.item_location.quantity:
            raise ValidationError(QUANTITY_EXCEEDS_AVAILABLE_ERROR)

    def save(self, *args, **kwargs):
        super(WriteOffItem, self).save(*args, **kwargs)
        if not ModelMethods.is_update(self):
            success = QuantityManager.write_off(self.item_location, self.quantity)
            if not success:
                # дублюється перевірка, але поки можливо залишити її, щоб відловити інші можливі сценарії
                raise ValueError(QUANTITY_EXCEEDS_AVAILABLE_ERROR)


    def __str__(self):
        return self.item_location.item.name



# def create_objects():
#     # автозаповнення бази даних
#
#     ItemCategory.objects.update_or_create(name='Laptop')
#     ItemCategory.objects.update_or_create(name='Mechanical')
#     ItemCategory.objects.update_or_create(name='Electrical')
#     ItemCategory.objects.update_or_create(name='Tool')
#
#     Owner.objects.update_or_create(name='DEFIR')
#     Owner.objects.update_or_create(name='MAP')
#     Owner.objects.update_or_create(name='KLAKONA')
#
#     Location.objects.update_or_create(name='Стелаж 1')
#     Location.objects.update_or_create(name='Стелаж 2')
#     Location.objects.update_or_create(name='Цех')
#     Location.objects.update_or_create(name='Офіс')
#     Location.objects.update_or_create(name='Кладовка')
#
#     Supplier.objects.update_or_create(name='Metalvis')
#     Supplier.objects.update_or_create(name='Dinmark')
#     Supplier.objects.update_or_create(name='Rozetka')
#     Supplier.objects.update_or_create(name='Foxtrot')
#
#
# def clean_db():
#     ItemCategory.objects.all().delete()
#     Item.objects.all().delete()
#     Supplier.objects.all().delete()
#     Location.objects.all().delete()
#     Owner.objects.all().delete()
#     ItemCategory.objects.all().delete()
#     ShoppingCart.objects.all().delete()
#     ItemLocation.objects.all().delete()


# create_objects()
# clean_db()
