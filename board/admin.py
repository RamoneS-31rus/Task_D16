from django.contrib import admin
from .models import Category, Post, Comment


class AdminPost(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class AdminCategory(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category, AdminCategory)
admin.site.register(Post, AdminPost)
admin.site.register(Comment)
