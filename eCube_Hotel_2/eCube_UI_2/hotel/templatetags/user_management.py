from django import template

register = template.Library()


@register.filter
def snake_case(value):
    return "_".join(value.lower().split(' '))