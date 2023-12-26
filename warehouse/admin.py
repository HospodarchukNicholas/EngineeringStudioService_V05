from django.contrib import admin
from .models import *
from .forms import *



admin.site.site_header = 'DefirWarehouse_v0.3'
admin.site.site_title = 'DefirWarehouse_v0.3'

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    #дозволяє створити адмін модель але при цьому не відображати її в адмін панелі. Тобто дозволяє створювати обєкти з інших форм
    # list_display = ('name', 'value')
    def get_model_perms(self, request):
        return {}

# class ToolAdmin(admin.ModelAdmin):
#     model = Tool
#
#     def get_changeform_initial_data(self, request):
#         # дозволяє вставити автоматичне значення для foreig key
#         initial = super().get_changeform_initial_data(request)
#         initial['category'] = ItemCategory.objects.get(name='Tool')
#         return initial
#
# admin.site.register(Tool, ToolAdmin)

@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    #обов'язково потрібно добавляти в батькіську модель search_fields, щоб можна було зробити автозамовненння
    search_fields = ['name']
    #дозволяє створити адмін модель але при цьому не відображати її в адмін панелі. Тобто дозволяє створювати обєкти з інших форм
    def get_model_perms(self, request):
        return {}

@admin.register(Location)
class PlaceAdmin(admin.ModelAdmin):
    search_fields = ['name']
    #дозволяє створити адмін модель але при цьому не відображати її в адмін панелі. Тобто дозволяє створювати обєкти з інших форм
    def get_model_perms(self, request):
        return {}

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    search_fields = ['name']
    #дозволяє створити адмін модель але при цьому не відображати її в адмін панелі. Тобто дозволяє створювати обєкти з інших форм
    def get_model_perms(self, request):
        return {}

@admin.register(ShoppingCartItem)
class ShoppingCartItemAdmin(admin.ModelAdmin):
    list_display = ( 'name','integrated', 'category', 'quantity', 'product_link', 'supplier', 'brand', 'item_number', 'note', 'invoice_link', 'storage_place', 'owner')
    # search_fields = ['name']
    #дозволяє створити адмін модель але при цьому не відображати її в адмін панелі. Тобто дозволяє створювати обєкти з інших форм
    # def get_model_perms(self, request):
    #     return {}


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    search_fields = ['name']
    #дозволяє створити адмін модель але при цьому не відображати її в адмін панелі. Тобто дозволяє створювати обєкти з інших форм
    def get_model_perms(self, request):
        return {}

class ShoppingCartItemInline(admin.StackedInline):
     model = ShoppingCartItem
     fields = ( 'name', 'category', 'quantity', 'product_link', 'supplier', 'brand', 'item_number', 'note', 'invoice_link', 'storage_place', 'owner')
     list_display = ('name','cart', 'category', 'quantity', 'integrated',)
     extra = 1
     autocomplete_fields = ['category', 'storage_place', 'supplier']

# class ShoppingCartItemInline(admin.StackedInline):
#     #дозволяє автозаповнити поля даними з існуючого запису
#     model = ShoppingCartItem
#     form = ShoppingCartItemAdminForm
#     fields = ('existing_item', 'name', 'category', 'quantity', 'product_link', 'supplier', 'brand', 'item_number', 'note', 'invoice_link', 'storage_place', 'owner', )
#     extra = 1
#     autocomplete_fields = ['category', 'storage_place', 'supplier']
#
#     # class Media:
#     #     js = ('path/to/copy_item_data.js',)  # Include the JavaScript file
#
#     def get_formset(self, request, obj=None, **kwargs):
#         formset = super().get_formset(request, obj, **kwargs)
#
#         # Add a custom form media for the inline
#         # formset.Media.js += ('path/to/copy_item_data.js',)
#
#         return formset

class ShoppingCartAdmin(admin.ModelAdmin):
    inlines = [
        ShoppingCartItemInline
    ]
    list_display = ('purpose', 'status', 'id')

    def get_changeform_initial_data(self, request):
        # дозволяє вставити автоматичне значення для foreig key
        initial = super().get_changeform_initial_data(request)
        initial['created_by'] = request.user
        return initial

admin.site.register(ShoppingCart, ShoppingCartAdmin)
# admin.site.register(ShoppingCartItem)

class WriteOffItemInline(admin.StackedInline):
    model = WriteOffItem
    fields = ('item_location', 'quantity')
    extra = 1
    autocomplete_fields = ['item_location',]


class WriteOffAdmin(admin.ModelAdmin):
    inlines = [
        WriteOffItemInline
    ]
    list_display = ('reason', 'id')
    def get_changeform_initial_data(self, request):
        # дозволяє вставити автоматичне значення для foreig key
        initial = super().get_changeform_initial_data(request)
        initial['created_by'] = request.user
        return initial

admin.site.register(WriteOff, WriteOffAdmin)

@admin.register(ItemLocation)
class ItemLocationAdmin(admin.ModelAdmin):
    list_display = ('item', 'location', 'quantity', 'owner', 'id')
    search_fields = ['item', 'location']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'id',)