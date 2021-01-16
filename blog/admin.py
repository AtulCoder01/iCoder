from django.contrib import admin
from blog.models import Post, BlogComment

# Register your models here.
admin.site.register((BlogComment)) # we can also register like this


# here we inject javascript in tiny editer
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ('tinyInject.js',)  # this file is in /static/ dir
