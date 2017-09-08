from django.db import models
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
import re
import random
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100,verbose_name='类别')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='文章分类'
        verbose_name_plural='文章分类'

class DailyPost(models.Model):
    title = models.CharField(max_length=200)
    created_time = models.DateTimeField()
    body = models.TextField()
    excerpt = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey(User)
    image = models.ImageField(blank=True)
    views = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category)


    class Meta:
        verbose_name='文章'
        verbose_name_plural='文章'

    def __str__(self):
        return self.title

    def get_date(self):
        year = self.created_time.year
        month = self.created_time.month
        day = self.created_time.day
        date = '{}年{}月{}日'.format(year,month,day)
        return date

    def increase_views(self):
        self.views +=1
        self.save(update_fields=['views'])

    def get_absolute_url(self):
        return reverse('dailypost:detail',kwargs={'pk':self.pk})

    def save(self,*args,**kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:100]

        if not self.image:
            if re.findall(r'\!\[.*?\]\((.*?)\)',self.body,re.S):
                body_pics = re.findall(r'\!\[.*?\]\((.*?)\)',self.body,re.S)
                a = random.choice(0,len(body_pics))
                self.image=body_pics[a]
            else:
                self.image='../static/images/1.jpg'
        super(DailyPost,self).save(*args,**kwargs)

    def short_title(self):
        if len(self.title)> 14:
            short_title=self.title[0:13]+'...'
        else:
            short_title=self.title
        return short_title


class HiddenPost(models.Model):
    title = models.CharField(max_length=200)
    created_time = models.DateField()
    body = models.TextField()
    excerpt = models.CharField(max_length=200, blank=True)
    image = models.ImageField(blank=True)
    category = models.CharField(max_length=200)

    class Meta:
        verbose_name='隐藏文章'
        verbose_name_plural='隐藏文章'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('dailypost:hidden_detail',kwargs={'pk':self.pk})

    def save(self,*args,**kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:100]

        if not self.image:
            if re.findall(r'\!\[.*?\]\((.*?)\)',self.body,re.S):
                body_pics = re.findall(r'\!\[.*?\]\((.*?)\)',self.body,re.S)
                a = random.choice(0,len(body_pics))
                self.image=body_pics[a]
            else:
                self.image='../static/images/1.jpg'
        super(HiddenPost,self).save(*args,**kwargs)

    def short_title(self):
        if len(self.title)> 14:
            short_title=self.title[0:13]+'...'
        else:
            short_title=self.title
        return short_title
