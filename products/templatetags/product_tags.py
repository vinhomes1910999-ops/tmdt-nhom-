from django import template

register = template.Library()


@register.filter(name='vnd')
def vnd(value):
    """
    Format decimal or int to Vietnamese Dong format, e.g.: 362000 -> 362.000₫
    """
    if value is None or value == '':
        return '0₫'
    try:
        val = int(round(float(value)))
        formatted = f"{val:,}".replace(',', '.')
        return f"{formatted}₫"
    except (ValueError, TypeError):
        return f"{value}₫"


@register.filter(name='split_string')
def split_string(value, delimiter=','):
    """
    Splits string by delimiter and strips whitespace, returns list
    """
    if not value:
        return []
    return [item.strip() for item in str(value).split(delimiter) if item.strip()]


@register.filter(name='sub')
def sub(value, arg):
    """
    Subtracts arg from value
    """
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter(name='times')
def times(number):
    """
    Returns a range of numbers for rendering loops in templates, e.g. 5 stars
    """
    try:
        return range(int(number))
    except (ValueError, TypeError):
        return range(0)


@register.filter(name='star_rating')
def star_rating(rating):
    """
    Returns a list of booleans for 5 stars, True if filled, False if empty
    """
    try:
        r = round(float(rating or 0))
        return [i < r for i in range(5)]
    except (ValueError, TypeError):
        return [False] * 5
