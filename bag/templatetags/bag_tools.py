from decimal import Decimal, InvalidOperation
from django import template

register = template.Library()

@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    """
    Multiply price * quantity safely.
    """
    try:
        if price is None or quantity is None:
            return Decimal('0.00')
        # Ensure Decimal math
        price = Decimal(price)
        quantity = int(quantity)
        return (price * quantity).quantize(Decimal('0.01'))
    except (InvalidOperation, ValueError, TypeError):
        return Decimal('0.00')