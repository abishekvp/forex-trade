from django import template
register = template.Library()

@register.filter
def total_price(cart_items):
    return sum(item.product.price for item in cart_items)