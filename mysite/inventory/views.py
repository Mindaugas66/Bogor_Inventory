from django.db.models import Count
import json
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
import datetime
from django.shortcuts import redirect
from .models import SatinSilk, Decorations, Materials, Products, Clients, Orders, OrderLines
from django.shortcuts import render

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
    orders_data = Orders.objects.filter(order_status='c', order_date__gte=start_of_week).values('order_date').annotate(order_count=Count('id'))

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
