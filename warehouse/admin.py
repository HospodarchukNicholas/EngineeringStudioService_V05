from django.contrib import admin
from .models import *
from django.utils.html import format_html, mark_safe
from .forms import *
import os
from pathlib import Path

VERSION = 'v0.5'
COMPANY_NAME = 'Defir'
admin.site.site_header = f'{COMPANY_NAME} Warehouse {VERSION}'
admin.site.site_title = f'{COMPANY_NAME} Warehouse {VERSION}'


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
    list_display = ('name', 'integrated', 'category', 'quantity', 'product_link',
                    'supplier', 'brand', 'item_number', 'note', 'invoice_link',
                    'storage_place', 'owner')
    # search_fields = ['name']


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


# admin.site.register(ShoppingCartItem)

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
    search_fields = ['item', 'location']




class ItemAdmin(admin.ModelAdmin):

    # def image_tag(self, obj):
    #     if obj.image:
    #         return format_html('<img src="{}"/>'.format(obj.image.url))
    #     else:
    #         return "No Photo"
    list_display = ('name', 'id', 'image', 'img_preview')
    readonly_fields = ('img_preview',)

    # def image_tag(self, obj):
    #     if obj.image:
    #         return mark_safe('<img src = "{url}" witdh = "{width}" height="{height}"/>'.format(
    #          url = obj.image.url,
    #          width = obj.image.width,
    #          height = obj.image.height
    #      ))
    #     else:
    #         return "No Photo"




    # def display_photo(self, obj):
    #     if obj.photo:
    #         return format_html('<img src="{}" width="50" height="50" />', obj.photo.url)
    #     else:
    #         return "No Photo"

    # def display_photo(self, obj):
    #     return format_html('<img src="{}" width="50" height="50" />', obj.photo.url)

    # image_tag.short_description = 'Photo Preview'
admin.site.register(Item, ItemAdmin)