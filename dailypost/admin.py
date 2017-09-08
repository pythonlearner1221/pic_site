from django.contrib import admin
from .models import DailyPost,Category,HiddenPost
# Register your models here.




class PostAdmin(admin.ModelAdmin):
    list_display = ['title','created_time','category','author']
    search_fields = ('title',)
    ordering = ('-created_time','category')

class CatAdmin(admin.ModelAdmin):
    list_display = ['name',]

class HiddenPostAdmin(admin.ModelAdmin):
    list_display = ['title','created_time','category']
    search_fields = ('title',)
    ordering = ('-created_time','category')

admin.site.register(DailyPost,PostAdmin)
admin.site.register(Category,CatAdmin)
admin.site.register(HiddenPost,HiddenPostAdmin)