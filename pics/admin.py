from django.contrib import admin
from .models import Pics
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','created_time','image_tag','likes']
    list_display_links = ['title','image_tag']
    list_filter = ('hidden','tags','category')
    fields = ('title','large_image_tag','tags',('category','hidden'),('pic_index','pic_size','likes'))
    date_hierarchy = 'created_time'
    list_per_page = 20
    search_fields = ('title','url')
    ordering=('-id','-created_time',)
    filter_horizontal = ('tags',)
    readonly_fields = ('image_tag','large_image_tag')

class PicAdmin(admin.ModelAdmin):
    list_display = ['title','image_tag']
    fields = ('image_tag','title')
    search_fields = ('title',)
    readonly_fields = ('image_tag',)
    ordering=('-id','title',)
    list_per_page=20

admin.site.register(Pics,PostAdmin)

