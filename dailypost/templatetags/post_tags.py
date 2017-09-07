from ..models import DailyPost,Category
from django import template
from django.db.models.aggregates import Count
from django.utils import timezone

register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):
    return DailyPost.objects.all().order_by('-created_time','category')[:num]

@register.simple_tag
def archives():
    year_info = timezone.now().year
    return DailyPost.objects.filter(created_time__year=year_info).dates('created_time','month',order='DESC')

@register.simple_tag
def archives_year():
    year_info = timezone.now().year
    return DailyPost.objects.filter(created_time__year__lt=year_info).dates('created_time','year',order='DESC')

@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('dailypost')).filter(num_posts__gt=0).order_by('id')
