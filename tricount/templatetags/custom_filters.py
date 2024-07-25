from django import template

register = template.Library()

@register.filter
def custom_abs(value):
    return abs(value)
