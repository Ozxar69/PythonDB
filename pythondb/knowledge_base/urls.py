from django.urls import path
from . import views


app_name = "knowledge_base"


urlpatterns = [
    path('', views.main, name="main"),
    path('<slug:category_slug>/', views.category, name='category'),
    path('<slug:category_slug>/<int:subcategory_id>/', views.post, name='post'),
    path('<slug:category_slug>/<int:subcategory_id>/create/', views.create_post, name='create_post'),

]