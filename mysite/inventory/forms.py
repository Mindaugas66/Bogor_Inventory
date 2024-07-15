from django import forms
from django.forms.models import inlineformset_factory
from .models import Orders, OrderLines, Clients, SatinSilk, Decorations, Materials
from datetime import date

class ClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ['first_name', 'last_name']

class OrderForm(forms.ModelForm):
    order_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=date.today
    )

    class Meta:
        model = Orders
        fields = ['order_date', 'order_status']

class OrderLineForm(forms.ModelForm):
    class Meta:
        model = OrderLines
        fields = ['product_id', 'quantity', 'deco_id']

OrderLineFormSet = inlineformset_factory(Orders, OrderLines, form=OrderLineForm, extra=1)

class RestockSatinSilkForm(forms.ModelForm):
    class Meta:
        model = SatinSilk
        fields = ["remaining_stock"]

class AddNewSatinSilkForm(forms.ModelForm):
    class Meta:
        model = SatinSilk
        fields = ['color', 'remaining_stock']

class RestockDecorationsForm(forms.ModelForm):
    class Meta:
        model = Decorations
        fields = ['remaining_stock']

class AddNewDecorationsForm(forms.ModelForm):
    class Meta:
        model = Decorations
        fields = ['deco_name', 'remaining_stock', 'cost_per_item', 'sell_price']

class RestockMaterialsForm(forms.ModelForm):
    class Meta:
        model = Materials
        fields = ['remaining_stock']

class AddNewMaterialsForm(forms.ModelForm):
    class Meta:
        model = Materials
        fields = ['material_name', 'remaining_stock']