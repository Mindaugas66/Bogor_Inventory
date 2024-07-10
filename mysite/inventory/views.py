from django.http import HttpResponse
from .models import SatinSilk, Decorations, Materials, Products, Clients, Orders, OrderLines, Profits
from django.shortcuts import render
def index(request):
    total_orders = Orders.objects.all().count()
    total_products = Products.objects.all().count()
    total_clients = Clients.objects.all().count()
    context = {
        'total_orders': total_orders,
        'total_products': total_products,
        'total_clients': total_clients
    }
    return render(request, 'index.html', context=context)