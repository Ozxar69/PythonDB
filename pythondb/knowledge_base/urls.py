from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    path('', views.main, name="main"),
    path('<slug:category_slug>/', views.category, name='category'),
    path('<slug:category_slug>/<int:subcategory_id>/', views.post, name='post'),


]