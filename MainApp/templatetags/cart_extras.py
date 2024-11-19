from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """
    Multiplica dos valores.
    """
    try:
        return value * arg
    except (ValueError, TypeError):
        return 0
