from django import forms
from django.forms.models import inlineformset_factory
from .models import Orders, OrderLines, Clients
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
