from django.contrib import admin
from .models import Category, SubCategory, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_filter = ('author_id', ' category_id', 'subcategory_id')