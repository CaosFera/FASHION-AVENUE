from rest_framework import serializers
from .models import Category, Products
from django.urls import reverse

class CategorySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['url','id', 'name', 'description', 'slug', 'active', 'created_at', 'updated_at']
        
    def get_url(self, obj):
        request = self.context.get('request')
        url = reverse('category-detail', kwargs={'slug': obj.slug, 'id': obj.id})
        return request.build_absolute_uri(url)


class ProductsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  
    url = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = ['url', 'id', 'name', 'price', 'image', 'slug', 'description', 'stock', 'size', 'color', 'category', 'active', 'created_at', 'updated_at']

    def get_url(self, obj):
        request = self.context.get('request')
        url = reverse('product-detail', kwargs={'category_slug': obj.category.slug, 'category_id': obj.category.id, 'product_slug': obj.slug, 'product_id': obj.id})
        return request.build_absolute_uri(url)


class CartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()