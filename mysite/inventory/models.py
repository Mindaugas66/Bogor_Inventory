from django.db import models
from django.dispatch import receiver


class SatinSilk(models.Model):
    color = models.CharField('Colour', max_length=20)
    remaining_stock = models.FloatField('Remaining (m)')
    cost_per_meter = models.FloatField('Cost per meter', default=0.10)
    one_flower_materials = models.FloatField('One flower materials', default=1.6, null=False)

    def __str__(self):
        return f"{self.color} Rose"

    class Meta:
        verbose_name = 'Satin Silk'
        verbose_name_plural = 'Satin Silks'


class Decorations(models.Model):
    deco_name = models.CharField('Name', max_length=20)
    remaining_stock = models.IntegerField('Remaining stock')
    cost_per_item = models.FloatField('Cost per item')
    sell_price = models.FloatField('Sell price')

    def __str__(self):
        return f"{self.deco_name} ({self.sell_price} €)"

    class Meta:
        verbose_name = 'Decoration'
        verbose_name_plural = 'Decorations'


class Materials(models.Model):
    material_name = models.CharField('Name', max_length=20)
    remaining_stock = models.IntegerField('Remaining stock')
    cost_per_item = models.FloatField('Cost per item', default=0.30)

    def __str__(self):
        return f"{self.material_name} {self.remaining_stock}"

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materials'


class Products(models.Model):
    silk_id = models.ForeignKey(SatinSilk, on_delete=models.CASCADE)
    product_id = models.CharField('Product ID', max_length=20, null=True, blank=True)
    cost_per_item = models.FloatField('Cost per item', default=1.30)

    def __str__(self):
        return f"{self.silk_id} {self.cost_per_item} €"

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Clients(models.Model):
    first_name = models.CharField('First name', max_length=20)
    last_name = models.CharField('Last name', max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['first_name', 'last_name']


class Orders(models.Model):
    order_date = models.DateField('Order date')
    client_id = models.ForeignKey(Clients, on_delete=models.CASCADE)
    ORDER_STATUS = (
        ('c', 'Completed'),
        ('i', 'In Progress'),
        ('x', 'Canceled'),
    )
    order_status = models.CharField(max_length=1, choices=ORDER_STATUS, default='i')

    def __str__(self):
        return f"{self.order_status} {self.client_id}"

    def order_total(self):
        result = 0
        for line in self.lines.all():
            result += line.price()
        return round(result, 2)

    def total_cost_to_make(self):
        result = 0
        total_flowers = 0

        for line in self.lines.all():
            result += line.cost_to_make()
            total_flowers += line.quantity

        # Calculate wrapping paper cost
        wrapping_paper_needed = self.calculate_wrapping_paper(total_flowers)
        wrapping_paper_cost = wrapping_paper_needed * 0.25  # Assuming each wrapping paper costs 0.25
        result += wrapping_paper_cost

        return round(result, 2)

    def calculate_wrapping_paper(self, total_flowers):
        if total_flowers <= 10:
            return 2
        elif total_flowers <= 25:
            return 3
        elif total_flowers <= 50:
            return 5
        else:
            return 7

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def profit_made(self):
        profit = self.order_total() - self.total_cost_to_make()
        return round(profit, 2)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderLines(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE, null=True, related_name='lines')
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(verbose_name='Quantity')
    materials = models.ForeignKey(SatinSilk, on_delete=models.CASCADE, null=True, blank=True)
    deco_id = models.ForeignKey(Decorations, on_delete=models.CASCADE, null=True, blank=True)

    def price(self):
        price = self.product_id.cost_per_item * self.quantity
        totalprice = price
        if self.deco_id:
            totalprice += self.deco_id.sell_price
        return round(totalprice, 2)

    def cost_to_make(self):
        cost = 0.36 * self.quantity
        totalcost = cost
        if self.deco_id:
            totalcost += self.deco_id.cost_per_item
        return round(totalcost, 2)

    def __str__(self):
        return f"{self.quantity} {self.deco_id}"

    class Meta:
        verbose_name = 'Order Line'
        verbose_name_plural = 'Order Lines'

from .signals import update_stock