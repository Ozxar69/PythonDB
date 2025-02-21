from rest_framework import serializers

from knowledge_base.models import Category, SubCategory, Post


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'id', 'description')


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'category')



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'category', 'subcategory']
        extra_kwargs = {
            'author': {'read_only': True},
            'category': {'required': False, 'write_only': True},
            'subcategory': {'required': False, 'write_only': True},
        }