from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_amount(item):
    # Check if the item has an 'amount' attribute (for Plan) or 'unit_amount' (for Price)
    return getattr(item, 'amount', None) or getattr(item, 'unit_amount', None)

@register.filter
def cart_total(cart_items):
    """
    Calculate the total cost of the cart.
    """
    return sum(
        item.quantity * item.product.prices.first().unit_amount for item in cart_items if item.product.prices.exists()
    )

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def currency(value):
    """Format a number as currency with commas and two decimal places."""
    try:
        # Convert from cents to main currency unit
        value = float(value) / 100
        return f"£{value:,.2f}"
    except (ValueError, TypeError):
        return value  # Return the original value if conversion fails

@register.filter
def sum_prices(items):
    return sum(item.price.unit_amount * item.quantity for item in items)