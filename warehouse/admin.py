from django.contrib import admin
from .models import *
from .modules.images import *
from .modules.constants import *

admin.site.site_header = f'{DEFAULT_COMPANY_NAME} Warehouse {PROJECT_VERSION}'
admin.site.site_title = f'{DEFAULT_COMPANY_NAME} Warehouse {PROJECT_VERSION}'

@admin.register(AttributeName)
class AttributeNameAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
            def get_model_perms() allows you to create an admin model
            but not display it in the admin panel. That is, it allows you to create objects from other forms
        """
        return {}

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
            def get_model_perms() allows you to create an admin model
            but not display it in the admin panel. That is, it allows you to create objects from other forms
        """
        return {}


@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    # it is necessary to add search fields to the parent model so that autofill can be done
    search_fields = ['name']

    def get_model_perms(self, request):
        """
            def get_model_perms() allows you to create an admin model
            but not display it in the admin panel. That is, it allows you to create objects from other forms
        """
        return {}


@admin.register(Location)
class PlaceAdmin(admin.ModelAdmin):
    search_fields = ['name']

    def get_model_perms(self, request):
        """
            def get_model_perms() allows you to create an admin model
            but not display it in the admin panel. That is, it allows you to create objects from other forms
        """
        return {}


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    search_fields = ['name']

    def get_model_perms(self, request):
        """
            def get_model_perms() allows you to create an admin model
            but not display it in the admin panel. That is, it allows you to create objects from other forms
        """
        return {}


@admin.register(ShoppingCartItem)
class ShoppingCartItemAdmin(admin.ModelAdmin):

    list_display = ('name', 'cart_purpose', 'integrated',
                    'category', 'quantity', 'product_link',
                    'supplier', 'brand', 'item_number',
                    'note', 'invoice_link', 'storage_place',
                    'owner')
    # search_fields = ['name']

    def cart_purpose(self, obj):
        # Return the "purpose" of the cart associated with the current ShoppingCartItem
        return obj.cart.purpose

    # Set a short description for the 'cart_purpose' method, which will be used as the column header in the list view
    cart_purpose.short_description = 'Cart Purpose'

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    search_fields = ['name']

    def get_model_perms(self, request):
        """
            def get_model_perms() allows you to create an admin model
            but not display it in the admin panel. That is, it allows you to create objects from other forms
        """
        return {}


class ShoppingCartItemInline(admin.StackedInline):
    model = ShoppingCartItem
    fields = (
        'name', 'category', 'quantity', 'product_link',
        'supplier', 'brand', 'item_number', 'note', 'invoice_link',
        'storage_place', 'owner'
    )
    list_display = ('name', 'cart', 'category', 'quantity', 'integrated',)
    autocomplete_fields = ['category', 'storage_place', 'supplier']
    extra = 1


class ShoppingCartAdmin(admin.ModelAdmin):
    inlines = [
        ShoppingCartItemInline
    ]
    list_display = ('purpose', 'status', 'id')

    def get_changeform_initial_data(self, request):
        """
            def get_changeform_initial_data() allows you to insert an automatic value for the foreign key
        """
        initial = super().get_changeform_initial_data(request)
        initial['created_by'] = request.user
        return initial


admin.site.register(ShoppingCart, ShoppingCartAdmin)


class WriteOffItemInline(admin.StackedInline):
    model = WriteOffItem
    fields = ('item_location', 'quantity')
    extra = 1
    autocomplete_fields = ['item_location', ]


class WriteOffAdmin(admin.ModelAdmin):
    inlines = [
        WriteOffItemInline
    ]
    list_display = ('reason', 'id')

    def get_changeform_initial_data(self, request):
        """
            def get_changeform_initial_data() allows you to insert an automatic value for the foreign key
        """
        initial = super().get_changeform_initial_data(request)
        initial['created_by'] = request.user
        return initial


admin.site.register(WriteOff, WriteOffAdmin)

@admin.register(ItemLocation)
class ItemLocationAdmin(admin.ModelAdmin):
    list_display = ('item', 'location', 'quantity', 'owner', 'id')
    search_fields = ('item', 'location', )


class ItemAdmin(admin.ModelAdmin):
    """
    Custom Admin class for managing Item objects in the Django admin interface.

    This class includes a custom method 'image_tag' to display an HTML image tag
    for the 'image' field, providing a preview in the list view.

    """

    def image_tag(self, obj):
        """
        Generate an HTML image tag using the 'image_tag' method from the ImageWizard class.

        Args:
            obj: The model object with an 'image' field.

        Returns:
            str: An HTML image tag with the specified width and automatic height.
                         If the object has no image, 'No preview image available' is displayed.
        """
        return ImageWizard.image_tag(obj)

    list_display = ('name', 'category', 'image_tag', 'id',)
    readonly_fields = ('image_tag',)
    list_per_page = 3  # Customize the number of items per page

    # Define a short description for the image_tag attribute
    image_tag.short_description = 'Preview image'
    image_tag.allow_tags = True

admin.site.register(Item, ItemAdmin)
