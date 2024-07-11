import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from .models import OrderLines, SatinSilk, Products, Decorations, Materials

logger = logging.getLogger(__name__)


@receiver(post_save, sender=OrderLines)
def update_stock(sender, instance, **kwargs):
    logger.info(f"OrderLine saved: {instance}")

    # Update SatinSilk stock
    if instance.product_id:
        silk = instance.product_id.silk_id
        materials_used = silk.one_flower_materials * instance.quantity
        logger.info(f"Materials used: {materials_used}")

        silk.remaining_stock -= materials_used
        silk.save()
        logger.info(f"Updated remaining stock: {silk.remaining_stock}")

    # Update Decorations stock
    if instance.deco_id:
        deco = instance.deco_id
        deco.remaining_stock -= 1  # Always 1 per order line
        deco.save()
        logger.info(f"Updated decoration stock: {deco.deco_name} now has {deco.remaining_stock} left")

    # Update Materials stock
    # Ensure this runs only once per Order save
    order = instance.order_id
    if order:
        total_flowers = OrderLines.objects.filter(order_id=order).aggregate(total=Sum('quantity'))['total']

        if total_flowers:
            logger.info(f"Total flowers in the order: {total_flowers}")

            # Update wrapping paper stock
            wrapping_paper_needed = calculate_wrapping_paper(total_flowers)
            wrapping_paper = Materials.objects.get(material_name='Wrapping paper')
            wrapping_paper.remaining_stock -= wrapping_paper_needed
            wrapping_paper.save()
            logger.info(
                f"Wrapping paper used: {wrapping_paper_needed}, remaining stock: {wrapping_paper.remaining_stock}")

            # Update production materials stock
            production_materials = Materials.objects.get(material_name='Production materials')
            production_materials.remaining_stock -= 1  # Always 1 per order
            production_materials.save()
            logger.info(f"Production materials used: 1, remaining stock: {production_materials.remaining_stock}")


def calculate_wrapping_paper(total_flowers):
    if total_flowers <= 10:
        return 2
    elif total_flowers <= 25:
        return 3
    elif total_flowers <= 50:
        return 5
    else:
        return 7
