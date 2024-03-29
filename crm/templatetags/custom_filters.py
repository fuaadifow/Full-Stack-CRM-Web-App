from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def checkScores(value, arg):
    return value*0.80 < arg