from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, PostViewSet, SubCategoryViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(
    r"(?P<category_id>\d+)/subcategories",
    SubCategoryViewSet,
    basename="subcategory",
)
router.register(
    r"subcategories/(?P<subcategory_id>\d+)/posts", PostViewSet, basename="post"
)

urlpatterns = [
    path("", include(router.urls)),
]
