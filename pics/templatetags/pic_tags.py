from ..models import Pics
from django import template
from django.utils import timezone


register = template.Library()

@register.simple_tag
def archives():
    now = timezone.now().date()
    year = timezone.now().year
    return Pics.objects.filter(created_time__lte=now,created_time__year=year).dates('created_time','month',order='DESC')

@register.simple_tag
def archives_year():
    year = timezone.now().year
    return Pics.objects.filter(created_time__year__lt=year).dates('created_time','year',order='DESC')
