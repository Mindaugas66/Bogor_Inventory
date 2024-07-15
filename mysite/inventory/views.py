from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
import json

from django.views import generic
from django.contrib.auth.decorators import login_required
import datetime
from django.shortcuts import redirect, get_object_or_404
from .models import SatinSilk, Decorations, Materials, Products, Clients, Orders, OrderLines
from django.shortcuts import render
from .forms import OrderForm, OrderLineFormSet, ClientForm, RestockSatinSilkForm, AddNewSatinSilkForm, \
    RestockDecorationsForm, AddNewDecorationsForm, RestockMaterialsForm, AddNewMaterialsForm
from django.core.paginator import Paginator


@login_required(login_url='/accounts/login/')
def redirect_to_dashboard(request):
    return redirect('index')


@login_required(login_url='/accounts/login/')
def index(request):
    total_orders = Orders.objects.all().count()
    total_products = Products.objects.all().count()
    total_clients = Clients.objects.all().count()
    now = datetime.datetime.now()
    current_month = now.month
    current_year = now.year
    previous_month = (now.month - 1) if now.month > 1 else 12
    previous_year = now.year if now.month > 1 else now.year - 1
    current_month_orders = Orders.objects.filter(
        order_status='c',
        order_date__year=current_year,
        order_date__month=current_month
    )
    previous_month_orders = Orders.objects.filter(
        order_status='c',
        order_date__year=previous_year,
        order_date__month=previous_month
    )
    total_earnings_current = round(sum(order.order_total() for order in current_month_orders), 2)
    total_earnings_previous = round(sum(order.order_total() for order in previous_month_orders), 2)
    total_expenses_current = round(sum(order.total_cost_to_make() for order in current_month_orders), 2)
    total_expenses_previous = round(sum(order.total_cost_to_make() for order in previous_month_orders), 2)
    total_profit_current = round(sum(order.profit_made() for order in current_month_orders), 2)
    total_profit_previous = round(sum(order.profit_made() for order in previous_month_orders), 2)
    difference_earnings = total_earnings_current - total_earnings_previous
    difference_expenses = total_expenses_current - total_expenses_previous
    difference_profit = total_profit_current - total_profit_previous
    difference_earnings_percentage = round((difference_earnings / total_earnings_current) * 100, 2)
    difference_expenses_percentage = round((difference_expenses / total_expenses_current) * 100, 2)
    difference_profit_percentage = round((difference_profit / total_profit_current) * 100, 2)

    # Calculate number of orders per day for the current week
    start_of_week = now - datetime.timedelta(days=now.weekday())
    orders_data = Orders.objects.filter(order_status='c', order_date__gte=start_of_week).values('order_date').annotate(
        order_count=Count('id'))

    # Prepare data for the chart, ensuring all days of the week are included
    orders_dict = {order['order_date'].strftime('%A'): order['order_count'] for order in orders_data}
    week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    orders_chart_data = [{'day': day, 'order_count': orders_dict.get(day, 0)} for day in week_days]

    context = {
        "orders_data": json.dumps(orders_chart_data),  # Pass orders data as JSON
        "difference_earnings_percentage": difference_earnings_percentage,
        "difference_expenses_percentage": difference_expenses_percentage,
        "difference_profit_percentage": difference_profit_percentage,
        'total_orders': total_orders,
        'total_products': total_products,
        'total_clients': total_clients,
        'total_earnings_current': total_earnings_current,
        'total_earnings_previous': total_earnings_previous,
        'total_expenses_current': total_expenses_current,
        'total_expenses_previous': total_expenses_previous,
        'total_profit_current': total_profit_current,
        'total_profit_previous': total_profit_previous,
        'year': current_year,
    }
    return render(request, 'index.html', context=context)


@login_required(login_url='/accounts/login/')
def orders(request):
    orders = Orders.objects.all().order_by('-order_date')
    paginator = Paginator(orders, per_page=15)
    page_number = request.GET.get("page")
    paged_orders = paginator.get_page(page_number)
    context = {
        "orders": paged_orders,
    }
    return render(request, template_name="orders.html", context=context)


def order_view(request, order_id):
    order_instance = get_object_or_404(Orders, pk=order_id)
    order_lines = OrderLines.objects.filter(order_id=order_instance)
    context = {
        "order": order_instance,
        "order_lines": order_lines,
    }
    return render(request, template_name="order.html", context=context)


class OrderDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Orders
    success_url = "/orders/"
    context_object_name = "order"
    template_name = 'order_delete.html'


@login_required(login_url='/accounts/login/')
def new_order(request):
    if request.method == 'POST':
        client_form = ClientForm(request.POST)
        order_form = OrderForm(request.POST)
        formset = OrderLineFormSet(request.POST, instance=Orders())

        if client_form.is_valid() and order_form.is_valid() and formset.is_valid():
            client = client_form.save()
            order = order_form.save(commit=False)
            order.client_id = client
            order.save()
            order_lines = formset.save(commit=False)
            for line in order_lines:
                line.order_id = order
                line.save()
            return redirect('orders')
    else:
        client_form = ClientForm()
        order_form = OrderForm()
        formset = OrderLineFormSet(instance=Orders())

    return render(request, 'new_order.html', {'client_form': client_form, 'order_form': order_form, 'formset': formset})


@login_required(login_url='/accounts/login/')
def edit_order(request, pk):
    order = get_object_or_404(Orders, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        formset = OrderLineFormSet(request.POST, instance=order)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('orders')
    else:
        form = OrderForm(instance=order)
        formset = OrderLineFormSet(instance=order)
    return render(request, 'order_edit.html', {'form': form, 'formset': formset})


@login_required(login_url='/accounts/login/')
def inventory(request):
    flowers = SatinSilk.objects.all()
    decorations = Decorations.objects.all()
    wrapping_paper = Materials.objects.all()
    return render(request, 'inventory.html', {
        'flowers': flowers,
        'decorations': decorations,
        'wrapping_paper': wrapping_paper
    })


def restock_satin_silk(request, pk):
    satin_silk = get_object_or_404(SatinSilk, pk=pk)
    if request.method == "POST":
        form = RestockSatinSilkForm(request.POST, instance=satin_silk)
        if form.is_valid():
            form.save()
            return redirect('inventory')  # Update with your inventory view name
    else:
        form = RestockSatinSilkForm(instance=satin_silk)
    return render(request, 'restock_satin_silk.html', {'form': form})

def add_new_satin_silk(request):
    if request.method == "POST":
        form = AddNewSatinSilkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory')  # Update with your inventory view name
    else:
        form = AddNewSatinSilkForm()
    return render(request, 'add_new_satin_silk.html', {'form': form})

def restock_decorations(request, pk):
    decoration = get_object_or_404(Decorations, pk=pk)
    if request.method == "POST":
        form = RestockDecorationsForm(request.POST, instance=decoration)
        if form.is_valid():
            form.save()
            return redirect('inventory')  # Update with your inventory view name
    else:
        form = RestockDecorationsForm(instance=decoration)
    return render(request, 'restock_decorations.html', {'form': form})

def add_new_decorations(request):
    if request.method == "POST":
        form = AddNewDecorationsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory')  # Update with your inventory view name
    else:
        form = AddNewDecorationsForm()
    return render(request, 'add_new_decorations.html', {'form': form})

def restock_materials(request, pk):
    material = get_object_or_404(Materials, pk=pk)
    if request.method == "POST":
        form = RestockMaterialsForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect('inventory')  # Update with your inventory view name
    else:
        form = RestockMaterialsForm(instance=material)
    return render(request, 'restock_materials.html', {'form': form})

def add_new_materials(request):
    if request.method == "POST":
        form = AddNewMaterialsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory')  # Update with your inventory view name
    else:
        form = AddNewMaterialsForm()
    return render(request, 'add_new_materials.html', {'form': form})