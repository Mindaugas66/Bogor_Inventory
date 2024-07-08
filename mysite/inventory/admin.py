from django.contrib import admin
from .models import SatinSilk, Decorations, Materials, Products, OrderLines, Clients, Orders, Profits


# Register your models here.

class SatinSilkAdmin(admin.ModelAdmin):
    list_display = ['color', "remaining_stock", "cost_per_meter"]


class DecorationsAdmin(admin.ModelAdmin):
    list_display = ['deco_name', "remaining_stock", "sell_price"]


class MaterialsAdmin(admin.ModelAdmin):
    list_display = ['material_name', "remaining_stock", "cost_per_item"]


class ProductsAdmin(admin.ModelAdmin):
    list_display = ['silk_id', "cost_per_item"]


class OrderLinesAdmin(admin.ModelAdmin):
    list_display = ["product_id", "deco_id", "quantity", 'price']

class OrderlinesInLine(admin.TabularInline):
    model = OrderLines
    extra = 0
    fields = ["product_id", 'quantity', 'deco_id']


class ClientsAdmin(admin.ModelAdmin):
    list_display = ['first_name', "last_name"]


class OrdersAdmin(admin.ModelAdmin):
    list_display = ["client_id", "order_status", "total"]
    inlines = [OrderlinesInLine]


class ProfitsAdmin(admin.ModelAdmin):
    list_display = ['order_id', "total_cost", "total_sell_price", "profit"]


admin.site.register(SatinSilk, SatinSilkAdmin)
admin.site.register(Decorations, DecorationsAdmin)
admin.site.register(Materials, MaterialsAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(OrderLines, OrderLinesAdmin)
admin.site.register(Clients, ClientsAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(Profits, ProfitsAdmin)
