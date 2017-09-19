from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
import markdown
from django.utils.html import strip_tags
import re
import random
from django.utils.safestring import mark_safe
# Create your models here.


class Tags(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Pics(models.Model):
    title = models.CharField(max_length=200,blank=True)
    url = models.URLField(max_length=200,blank=True)
    created_time = models.DateField(auto_now_add=True)
    likes = models.IntegerField(default=0,blank=True)
    category = models.CharField(max_length=100, blank=True)
    hidden = models.IntegerField(default=0,blank=True)
    pic_index = models.CharField(max_length=200,blank=True,null=True)
    tags = models.ManyToManyField(Tags,blank=True)
    pic_size = models.PositiveIntegerField(blank=True,default=0)
    hashcode = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.title[:20]

    def image_tag(self):
        return mark_safe(u'<img src="%s" style="height:100px"/>' % self.url)

    def large_image_tag(self):
        return mark_safe(u'<img src="%s" />' % self.url)

    image_tag.short_description = 'Image'

    def next(self):
        try:
            return Pics.objects.filter(id__gt=self.id,hidden=0).order_by('id')[0]
        except:
            return None

    def previous(self):
        try:
            return Pics.objects.filter(id__lt=self.id,hidden=0).order_by('-id')[0]
        except:
            return None

    def save(self,*args,**kwargs):
        super(Pics, self).save(*args, **kwargs)
        if self.hidden==1 :
            if self.category=='pic':
                self.tags.add(Tags.objects.get(name='妹子图片'))

            if self.category=='gif':
                self.tags.add(Tags.objects.get(name='妹子动图'))
        else:
            self.tags.add(Tags.objects.get(name='其他'))

