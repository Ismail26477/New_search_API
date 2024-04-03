from django import template

register = template.Library()

@register.filter
def split_by_star(value):
    return value.split('*')