from django.contrib import admin
from .models import Post
from .forms import PostModelForm


class PostModelAdmin(admin.ModelAdmin):
    form = PostModelForm


admin.site.register(Post, PostModelAdmin)
