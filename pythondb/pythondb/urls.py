from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.urls import include, path

from knowledge_base.views import CategoryViewSet, SubCategoryViewSet, \
    PostViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'categories/(?P<category_id>\d+)/subcategories', SubCategoryViewSet, basename='subcategory')
router.register(r'subcategories/(?P<subcategory_id>\d+)/posts', PostViewSet, basename='post')

urlpatterns = [

    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("", include("knowledge_base.urls")),
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.jwt')),

]
