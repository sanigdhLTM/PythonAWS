from django.contrib import admin
from .models import Blog, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_id", "category_name", "is_deleted")


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("blog_id", "blog_title", "category", "views", "is_deleted")