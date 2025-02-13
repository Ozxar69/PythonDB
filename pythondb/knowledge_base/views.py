from django.shortcuts import render, get_object_or_404
from .models import Category, Post

from data import CATEGORY, SUBCATEGORIES, CATEGORIES, PATH_POST, \
    PATH_CATEGORIES, PATH_MAIN, POSTS_BY_SUBCATEGORY, POSTS


def get_objects(category_slug) -> dict:
    category = get_object_or_404(Category, slug=category_slug)
    categories = Category.objects.all()
    subcategories = category.subcategories.all()
    return {
        CATEGORY: category,
        SUBCATEGORIES: subcategories,
        CATEGORIES: categories,
    }


def main(request):
    categories = Category.objects.all()
    return render(request, PATH_MAIN, {CATEGORIES: categories})


def category(request, category_slug):
    dict = get_objects(category_slug)
    posts_by_subcategory = {subcategory.id: subcategory.posts.all() for
                            subcategory in dict[SUBCATEGORIES]}
    return render(request, PATH_CATEGORIES, {
        CATEGORY: dict[CATEGORY],
        SUBCATEGORIES: dict[SUBCATEGORIES],
        CATEGORIES: dict[CATEGORIES],
        POSTS_BY_SUBCATEGORY: posts_by_subcategory,
    })


def post(request, subcategory_id, category_slug):
    dict = get_objects(category_slug)
    posts = Post.objects.filter(subcategory_id=subcategory_id)
    return render(request, PATH_POST, {
        POSTS: posts,
        SUBCATEGORIES: dict[SUBCATEGORIES],
        CATEGORIES: dict[CATEGORIES],
        CATEGORY: dict[CATEGORY],
    })

