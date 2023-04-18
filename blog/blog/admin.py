from django.contrib import admin
from . import models
from blog.models import Post
from django_summernote.admin import SummernoteModelAdmin

#admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('created', 'author', 'publish', 'status')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('body', )

admin.site.register(models.Post, PostAdmin)