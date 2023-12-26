# from django import forms
# from .models import *
#
# class ShoppingCartItemAdminForm(forms.ModelForm):
        #дозволяє автозаповнити поля даними з існуючого запису
#     class Meta:
#         model = ShoppingCartItem
#         fields = '__all__'
#
#     existing_item = forms.ModelChoiceField(
#         queryset=ShoppingCartItem.objects.all(),
#         required=False,
#         label='Choose an existing item',
#         widget=forms.Select(attrs={'onchange': 'copy_item_data(this);'}),
#     )
#
#     def clean(self):
#         cleaned_data = super().clean()
#         existing_item = cleaned_data.get('existing_item')
#
#         if existing_item:
#             cleaned_data['name'] = existing_item.name
#             cleaned_data['category'] = existing_item.category
#             cleaned_data['quantity'] = existing_item.quantity
#             cleaned_data['product_link'] = existing_item.product_link
#             cleaned_data['supplier'] = existing_item.supplier
#             cleaned_data['brand'] = existing_item.brand
#             cleaned_data['item_number'] = existing_item.item_number
#             cleaned_data['note'] = existing_item.note
#             cleaned_data['invoice_link'] = existing_item.invoice_link
#             cleaned_data['storage_place'] = existing_item.storage_place
#             cleaned_data['owner'] = existing_item.owner
#
#             # Mark the form as integrated to prevent further modification
#             cleaned_data['integrated'] = True
#
#         return cleaned_data