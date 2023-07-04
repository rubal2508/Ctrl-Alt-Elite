from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def round1(value):
    return round(value, 1)


@register.filter
def isDateGreater(value):
    return value > timezone.now()
