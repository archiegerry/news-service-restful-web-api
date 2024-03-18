from django.contrib import admin
from .models import Author, Story

class StoryAdmin(admin.ModelAdmin):
    list_display = ('headline', 'category', 'region', 'author', 'datetime', 'details')

admin.site.register(Author)
admin.site.register(Story, StoryAdmin)

# Register your models here.
