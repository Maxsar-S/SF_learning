from django.contrib import admin
from .models import Post, Author, Comment, Category, PostCategory

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'get_cat', 'time_create', 'rating')
    list_filter = ('author', 'post_category', 'rating')
    search_fiels = ('author', 'title', 'post_category', 'time_create', 'rating')


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(PostCategory)
