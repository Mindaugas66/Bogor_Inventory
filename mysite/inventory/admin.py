from django.contrib import admin
from .models import SatinSilk, Decorations, Materials, Products, OrderLines, Clients, Orders


# Register your models here.

class SatinSilkAdmin(admin.ModelAdmin):
    list_display = ['color', "remaining_stock", "cost_per_meter"]


class DecorationsAdmin(admin.ModelAdmin):
    list_display = ['deco_name', "remaining_stock", 'cost_per_item', "sell_price"]


class MaterialsAdmin(admin.ModelAdmin):
    list_display = ['material_name', "remaining_stock", "cost_per_item"]


class ProductsAdmin(admin.ModelAdmin):
    list_display = ['silk_id', "cost_per_item"]


class OrderLinesAdmin(admin.ModelAdmin):
    list_display = ["product_id", "deco_id", "quantity", 'price', 'cost_to_make']


class OrderlinesInLine(admin.TabularInline):
    model = OrderLines
    extra = 0
    fields = ["product_id", 'quantity', 'deco_id']


class ClientsAdmin(admin.ModelAdmin):
    list_display = ['first_name', "last_name"]


class OrdersAdmin(admin.ModelAdmin):
    list_display = ["formatted_order_date", "client_id", "order_status", "order_total", "total_cost_to_make", "profit_made"]
    inlines = [OrderlinesInLine]

    def formatted_order_date(self, obj):
        return obj.order_date.strftime('%Y-%m-%d')

    # Optionally, you can add a short description for the column header
    formatted_order_date.short_description = 'Order Date'


class ProfitsAdmin(admin.ModelAdmin):
    list_display = ['order_id', "total_cost", "total_sell_price", "profit"]


admin.site.register(SatinSilk, SatinSilkAdmin)
admin.site.register(Decorations, DecorationsAdmin)
admin.site.register(Materials, MaterialsAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(OrderLines, OrderLinesAdmin)
admin.site.register(Clients, ClientsAdmin)
admin.site.register(Orders, OrdersAdmin)
