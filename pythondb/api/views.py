from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.serializers import (
    CategorySerializer,
    PostSerializer,
    SubCategorySerializer,
)
from knowledge_base.decorators import author_required
from knowledge_base.models import Category, Post, SubCategory


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
