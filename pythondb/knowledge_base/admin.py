from django.contrib import admin

from .models import Category, Post, SubCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_filter = ("category", "id")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_filter = ("author", "category_id", "subcategory_id")
