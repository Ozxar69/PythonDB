from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Post, SubCategory
from .forms import PostForm
from data import CATEGORY, SUBCATEGORIES, CATEGORIES, PATH_POST, \
    PATH_CATEGORIES, PATH_MAIN, POSTS_BY_SUBCATEGORY, POSTS, SUBCATEGORY
from django.contrib.auth.decorators import login_required
import markdown2
import re


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
    subcategory = SubCategory.objects.filter(id=subcategory_id)
    for post in posts:
        post.content = markdown2.markdown(post.content)
        post.content = re.sub(r'```(.*?)```', r'<pre><code class="language-python">\1</code></pre>', post.content, flags=re.DOTALL)
        post.content = re.sub(r'\'\'\'(.*?)\'\'\'',
                          r'<pre><code class="language-python">\1</code></pre>',
                          post.content, flags=re.DOTALL)
    return render(request, PATH_POST, {
        POSTS: posts,
        SUBCATEGORIES: dict[SUBCATEGORIES],
        CATEGORIES: dict[CATEGORIES],
        CATEGORY: dict[CATEGORY],
        SUBCATEGORY: subcategory[0],
    })

@login_required
def create_post(request, category_slug, subcategory_id):
    category = get_object_or_404(Category, slug=category_slug)
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    print(category)
    print(subcategory)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.category = category
            post.subcategory = subcategory
            post.author = request.user
            post.save()
            return redirect('knowledge_base:post', category_slug=category.slug,
                            subcategory_id=subcategory.id)
    else:
        form = PostForm()

    return render(request, 'knowledge_base/created_post.html', {'form': form})