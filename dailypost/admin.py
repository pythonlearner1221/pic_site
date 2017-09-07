from django.contrib import admin
from .models import DailyPost,Category
# Register your models here.




class PostAdmin(admin.ModelAdmin):
    list_display = ['title','created_time','category','author']
    search_fields = ('title',)

class CatAdmin(admin.ModelAdmin):
    list_display = ['name',]

admin.site.register(DailyPost,PostAdmin)
admin.site.register(Category,CatAdmin)
