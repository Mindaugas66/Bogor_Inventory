from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
import datetime
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import password_validation
from django.views.generic.edit import FormMixin, UpdateView, CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import SatinSilk, Decorations, Materials, Products, Clients, Orders, OrderLines
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def redirect_to_dashboard(request):
    return redirect('index')


@login_required(login_url='/accounts/login/')
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