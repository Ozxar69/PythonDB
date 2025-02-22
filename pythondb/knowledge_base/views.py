import re

import markdown2
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from data import (
    CATEGORIES,
    CATEGORY,
    PATH_CATEGORIES,
    PATH_MAIN,
    PATH_POST,
    POSTS,
    POSTS_BY_SUBCATEGORY,
    SUBCATEGORIES,
    SUBCATEGORY,
)

from .decorators import author_required
from .forms import PostForm, SubcategoryForm
from .models import Category, Post, SubCategory, User
from .serializers import (
    CategorySerializer,
    PostSerializer,
    SubCategorySerializer,
)


def get_objects(category_slug) -> dict:
    """
    Получает данные, связанные с категорией, на основе её slug.

    **Параметры:**
    - `category_slug` (str): Уникальный идентификатор категории (slug), который используется для поиска категории.

    **Возвращает:**
    - dict: Словарь, содержащий:
        - `CATEGORY`: Объект категории.
        - `SUBCATEGORIES`: Все подкатегории, связанные с данной категорией.
        - `CATEGORIES`: Все категории в базе данных.

    **Что делает внутри:**
    - Ищет категорию по её slug. Если категория не найдена, возвращает ошибку 404.
    - Получает все категории из базы данных.
    - Получает все подкатегории, связанные с найденной категорией.
    - Возвращает словарь с данными.
    """
    category = get_object_or_404(Category, slug=category_slug)
    categories = Category.objects.all()
    subcategories = category.subcategories.all()

    return {
        CATEGORY: category,
        SUBCATEGORIES: subcategories,
        CATEGORIES: categories,
    }


def main(request):
    """
    Главная страница сайта, отображающая категории, последние посты, топ пользователей и статистику.

    **Параметры:**
    - `request` (HttpRequest): Объект запроса, содержащий данные о текущем запросе пользователя.

    **Возвращает:**
    - HttpResponse: HTML-страница, отрендеренная с данными для главной страницы.

    **Что делает внутри:**
    - Получает все категории из базы данных.
    - Получает последние 5 постов, включая связанные категории, подкатегории и авторов.
    - Получает топ-5 пользователей, отсортированных по количеству постов.
    - Считает общее количество категорий, подкатегорий и постов.
    - Рендерит страницу с переданными данными.
    """
    categories = Category.objects.all()

    latest_posts = Post.objects.select_related(
        "category", "subcategory", "author"
    ).order_by("-created_at")[:5]

    top_users = User.objects.annotate(post_count=Count("posts")).order_by(
        "-post_count"
    )[:5]

    total_categories = Category.objects.count()
    total_subcategories = SubCategory.objects.count()
    total_posts = Post.objects.count()

    return render(
        request,
        PATH_MAIN,
        {
            "categories": categories,
            "latest_posts": latest_posts,
            "top_users": top_users,
            "total_categories": total_categories,
            "total_subcategories": total_subcategories,
            "total_posts": total_posts,
        },
    )


def category(request, category_slug):
    """
    Отображает страницу категории с её описанием, подкатегориями и постами.

    **Параметры:**
    - `request` (HttpRequest): Объект запроса, содержащий данные о текущем запросе пользователя.
    - `category_slug` (str): Уникальный идентификатор категории (slug), который используется для поиска категории.

    **Возвращает:**
    - HttpResponse: HTML-страница, отрендеренная с данными о категории, подкатегориях и постах.

    **Что делает внутри:**
    - Вызывает функцию `get_objects`, чтобы получить данные о категории, подкатегориях и всех категориях.
    - Преобразует описание категории в HTML с помощью библиотеки `markdown2`.
    - Применяет регулярное выражение для форматирования кода Python в описании категории.
    - Создаёт словарь, где ключами являются ID подкатегорий, а значениями — связанные с ними посты.
    - Рендерит страницу категории с переданными данными.
    """
    dict = get_objects(category_slug)
    category = dict[CATEGORY]
    category.description = markdown2.markdown(category.description)
    category.description = re.sub(
        r"\'\'\'(.*?)\'\'\'",
        r'<pre><code class="language-python">\1</code></pre>',
        category.description,
        flags=re.DOTALL,
    )
    return render(
        request,
        PATH_CATEGORIES,
        {
            CATEGORY: category,
            SUBCATEGORIES: dict[SUBCATEGORIES],
            CATEGORIES: dict[CATEGORIES],
            POSTS_BY_SUBCATEGORY: {
                subcategory.id: subcategory.posts.all()
                for subcategory in dict[SUBCATEGORIES]
            },
        },
    )


def post(request, subcategory_id, category_slug):
    """
    Отображает страницу с постами, относящимися к определённой подкатегории.

    **Параметры:**
    - `request` (HttpRequest): Объект запроса, содержащий данные о текущем запросе пользователя.
    - `subcategory_id` (int): Уникальный идентификатор подкатегории.
    - `category_slug` (str): Уникальный идентификатор категории (slug), который используется для поиска категории.

    **Возвращает:**
    - HttpResponse: HTML-страница, отрендеренная с данными о постах, категории, подкатегории и связанных данных.

    **Что делает внутри:**
    - Вызывает функцию `get_objects`, чтобы получить данные о категории, подкатегориях и всех категориях.
    - Получает все посты, относящиеся к указанной подкатегории.
    - Форматирует содержимое каждого поста:
        - Применяет регулярное выражение для преобразования кода в HTML-блоки с подсветкой синтаксиса.
        - Преобразует содержимое поста в HTML с использованием библиотеки `markdown2`.
    - Рендерит страницу с переданными данными.
    """
    dict = get_objects(category_slug)
    posts = Post.objects.filter(subcategory_id=subcategory_id)
    subcategory = SubCategory.objects.filter(id=subcategory_id)

    for post in posts:
        post.content = post.content.strip()

        post.content = re.sub(
            r"'''(\w*)\s*(.*?)\s*'''",
            lambda match: f"<pre><code class='language-{match.group(1) or 'python'}'>{match.group(2).strip()}</code></pre>",
            post.content,
            flags=re.DOTALL,
        )

        post.content = re.sub(
            r"<(?!pre|code|/pre|/code).*?>",
            lambda match: f"&lt;{match.group(0)[1:-1]}&gt;",
            post.content,
        )

        post.content = markdown2.markdown(
            post.content, extras=["fenced-code-blocks", "code-friendly"]
        )

    return render(
        request,
        PATH_POST,
        {
            POSTS: posts,
            SUBCATEGORIES: dict[SUBCATEGORIES],
            CATEGORIES: dict[CATEGORIES],
            CATEGORY: dict[CATEGORY],
            SUBCATEGORY: subcategory[0],
        },
    )


@login_required
def create_post(request, category_slug, subcategory_id):
    """
    Создаёт новый пост в указанной категории и подкатегории.

    **Параметры:**
    - `request` (HttpRequest): Объект запроса, содержащий данные о текущем запросе пользователя.
    - `category_slug` (str): Уникальный идентификатор категории (slug), который используется для поиска категории.
    - `subcategory_id` (int): Уникальный идентификатор подкатегории.

    **Возвращает:**
    - HttpResponse: HTML-страница с формой для создания поста или перенаправление на страницу постов после успешного создания.

    **Что делает внутри:**
    - Вызывает функцию `get_objects`, чтобы получить данные о категории, подкатегориях и всех категориях.
    - Получает категорию и подкатегорию по их идентификаторам.
    - Если запрос является POST-запросом:
        - Проверяет валидность формы.
        - Создаёт новый пост, связывая его с категорией, подкатегорией и текущим пользователем.
        - Сохраняет пост и перенаправляет на страницу постов.
    - Если запрос не является POST-запросом, отображает пустую форму для создания поста.
    """
    dict = get_objects(category_slug)
    category = get_object_or_404(Category, slug=category_slug)
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    subcategory_name = SubCategory.objects.filter(id=subcategory_id)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.category = category
            post.subcategory = subcategory
            post.author = request.user
            post.save()
            return redirect(
                "knowledge_base:post",
                category_slug=category.slug,
                subcategory_id=subcategory.id,
            )
    else:
        form = PostForm()

    return render(
        request,
        "knowledge_base/created_post.html",
        {
            "form": form,
            SUBCATEGORIES: dict[SUBCATEGORIES],
            CATEGORIES: dict[CATEGORIES],
            CATEGORY: dict[CATEGORY],
            SUBCATEGORY: subcategory_name[0],
        },
    )


@login_required
@author_required
def edit_post(request, category_slug, subcategory_id, post_id):
    """
    Редактирует существующий пост.

    **Декораторы:**
    - `@login_required`: Требует, чтобы пользователь был авторизован.
    - `@autor_required`: Требует, чтобы пользователь был автором поста.

    **Параметры:**
    - `request` (HttpRequest): Объект запроса, содержащий данные о текущем запросе пользователя.
    - `category_slug` (str): Уникальный идентификатор категории (slug), к которой относится пост.
    - `subcategory_id` (int): ID подкатегории, к которой относится пост.
    - `post_id` (int): ID поста, который нужно отредактировать.

    **Возвращает:**
    - HttpResponse: HTML-страница с формой редактирования поста.

    **Что делает внутри:**
    - Получает данные о категории, подкатегории и посте.
    - Если запрос типа POST, проверяет и сохраняет изменения в посте.
    - Если запрос не POST, отображает форму редактирования с текущими данными поста.
    - Рендерит страницу с формой редактирования.
    """
    dict = get_objects(category_slug)
    subcategory_name = SubCategory.objects.filter(id=subcategory_id)
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(
                "knowledge_base:post",
                category_slug=category_slug,
                subcategory_id=subcategory_id,
            )
    else:
        form = PostForm(instance=post)
    return render(
        request,
        "knowledge_base/edit_post.html",
        {
            "form": form,
            SUBCATEGORIES: dict[SUBCATEGORIES],
            CATEGORIES: dict[CATEGORIES],
            CATEGORY: dict[CATEGORY],
            SUBCATEGORY: subcategory_name[0],
        },
    )


@login_required
@author_required
def delete_post(request, category_slug, subcategory_id, post_id):
    """
    Удаляет существующий пост.

    **Декораторы:**
    - `@login_required`: Требует, чтобы пользователь был авторизован.
    - `@autor_required`: Требует, чтобы пользователь был автором поста.

    **Параметры:**
    - `request` (HttpRequest): Объект запроса, содержащий данные о текущем запросе пользователя.
    - `category_slug` (str): Уникальный идентификатор категории (slug), к которой относится пост.
    - `subcategory_id` (int): ID подкатегории, к которой относится пост.
    - `post_id` (int): ID поста, который нужно удалить.

    **Возвращает:**
    - HttpResponse: Редирект на страницу подкатегории после удаления поста.
    - HttpResponseNotAllowed: Если запрос не POST, возвращает ошибку 405 (Method Not Allowed).

    **Что делает внутри:**
    - Получает пост по его ID.
    - Если запрос типа POST, удаляет пост и перенаправляет пользователя на страницу подкатегории.
    - Если запрос не POST, возвращает ошибку 405.
    """
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        post.delete()
        return redirect(
            "knowledge_base:post",
            category_slug=category_slug,
            subcategory_id=subcategory_id,
        )

    from django.http import HttpResponseNotAllowed

    return HttpResponseNotAllowed(["POST"])


def search(request):
    """
    Выполняет поиск по категориям, подкатегориям и постам.

    **Параметры:**
    - `request` (HttpRequest): Объект запроса, содержащий данные о текущем запросе пользователя.

    **Возвращает:**
    - HttpResponse: HTML-страница с результатами поиска, если запрос содержит поисковый запрос.
    - HttpResponseRedirect: Редирект на главную страницу, если запрос пустой.

    **Что делает внутри:**
    - Получает поисковый запрос из параметров GET.
    - Если запрос не пустой:
        - Выполняет поиск по категориям, подкатегориям и постам, используя `icontains`.
        - Формирует результаты поиска.
        - Рендерит страницу с результатами поиска.
    - Если запрос пустой, перенаправляет на главную страницу.
    """
    query = request.GET.get("q", "").strip()
    categories_items = Category.objects.all()
    if query:
        search_terms = query.split()

        category_query = Q()
        for term in search_terms:
            category_query |= Q(name__icontains=term) | Q(
                description__icontains=term
            )
        categories = Category.objects.filter(category_query).distinct()

        subcategory_query = Q()
        for term in search_terms:
            subcategory_query |= Q(name__icontains=term)
        subcategories = SubCategory.objects.filter(subcategory_query).distinct()

        post_query = Q()
        for term in search_terms:
            post_query |= Q(title__icontains=term) | Q(content__icontains=term)
        posts = Post.objects.filter(post_query).distinct()

        results = {
            "categories": categories,
            "subcategories": subcategories,
            "posts": posts,
        }
        return render(
            request,
            "knowledge_base/search_results.html",
            {
                "query": query,
                "results": results,
                CATEGORIES: categories_items,
            },
        )
    return redirect("knowledge_base:main")


@login_required
def like_post(request, post_id):
    """
    Переключает состояние "лайка" для поста.

    **Декораторы:**
    - `@login_required`: Требует, чтобы пользователь был авторизован.

    **Параметры:**
    - `request` (HttpRequest): Объект запроса, содержащий данные о текущем запросе пользователя.
    - `post_id` (int): ID поста, который нужно лайкнуть или убрать лайк.

    **Возвращает:**
    - HttpResponseRedirect: Редирект на предыдущую страницу (или на главную, если реферер отсутствует).

    **Что делает внутри:**
    - Получает пост по его ID.
    - Вызывает метод `toggle_like` для переключения состояния лайка.
    - Перенаправляет пользователя на предыдущую страницу.
    """
    post = get_object_or_404(Post, id=post_id)
    post.toggle_like(request.user)
    return redirect(request.META.get("HTTP_REFERER", "/"))


@staff_member_required
@login_required
def create_subcategory(request, category_slug):
    """
    Создаёт новую подкатегорию для указанной категории.

    **Декораторы:**
    - `@login_required`: Требует, чтобы пользователь был авторизован.
    - `@staff_member_required`: Требует, чтобы пользователь был сотрудником (staff).

    **Параметры:**
    - `request` (HttpRequest): Объект запроса, содержащий данные о текущем запросе пользователя.
    - `category_slug` (str): Уникальный идентификатор категории (slug), для которой создаётся подкатегория.

    **Возвращает:**
    - HttpResponse: HTML-страница с формой создания подкатегории.
    - HttpResponseRedirect: Редирект на страницу категории после успешного создания подкатегории.

    **Что делает внутри:**
    - Получает категорию по её slug.
    - Если запрос типа POST, проверяет и сохраняет новую подкатегорию.
    - Если запрос не POST, отображает пустую форму.
    - Рендерит страницу с формой создания подкатегории.
    """
    category = get_object_or_404(Category, slug=category_slug)
    dict = get_objects(category_slug)

    if request.method == "POST":
        form = SubcategoryForm(request.POST)
        if form.is_valid():
            subcategory = form.save(commit=False)
            subcategory.category = category
            subcategory.save()
            return redirect(
                "knowledge_base:category", category_slug=category_slug
            )
    else:
        form = SubcategoryForm()

    return render(
        request,
        "knowledge_base/create_subcategory.html",
        {
            "form": form,
            SUBCATEGORIES: dict[SUBCATEGORIES],
            CATEGORIES: dict[CATEGORIES],
            CATEGORY: dict[CATEGORY],
        },
    )


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        return SubCategory.objects.filter(category=category_id)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        subcategory_id = self.kwargs.get("subcategory_id")
        return Post.objects.filter(subcategory=subcategory_id)

    def perform_create(self, serializer):
        subcategory_id = self.kwargs.get("subcategory_id")
        subcategory = get_object_or_404(SubCategory, id=subcategory_id)

        serializer.save(
            author=self.request.user,
            subcategory=subcategory,
            category=subcategory.category,
        )

    @author_required
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @author_required
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
