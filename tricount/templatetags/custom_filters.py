from django import template

register = template.Library()

@register.filter(name='abs')
def abs_value(value):
    return abs(value)
