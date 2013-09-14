from django import template

register = template.Library()

@register.filter
def hexconvert(value):
    return "%x" % int(value)
