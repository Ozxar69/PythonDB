from django.urls import path

from . import views

app_name = "knowledge_base"


urlpatterns = [
    path("", views.main, name="main"),
    path("post/<int:post_id>/like/", views.like_post, name="like_post"),
    path("search/", views.search, name="search"),
    path("<slug:category_slug>/", views.category, name="category"),
    path("<slug:category_slug>/<int:subcategory_id>/", views.post, name="post"),
    path(
        "<slug:category_slug>/<int:subcategory_id>/create/",
        views.create_post,
        name="create_post",
    ),
    path(
        "<slug:category_slug>/create_subcategory/",
        views.create_subcategory,
        name="create_subcategory",
    ),
    path(
        "<slug:category_slug>/<int:subcategory_id>/<int:post_id>/edit_post/",
        views.edit_post,
        name="edit_post",
    ),
    path(
        "<slug:category_slug>/<int:subcategory_id>/<int:post_id>/delete_post/",
        views.delete_post,
        name="delete_post",
    ),
]
