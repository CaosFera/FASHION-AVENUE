from django.shortcuts import render, get_object_or_404
from .models import Category, Products
from .serializers import CategorySerializer, ProductsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .filters import CategoryFilter, ProductsFilter
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import CategoryPagination, ProductsPagination
from .cart import Cart

class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filterset_class = CategoryFilter  
    filter_backends = [DjangoFilterBackend]  
    pagination_class = CategoryPagination

    def get(self, request, *args, **kwargs):
        # Usa o queryset filtrado automaticamente pelo filterset
        categories = self.filter_queryset(self.get_queryset())
        
        # Usar a paginação
        page = self.paginate_queryset(categories)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(categories, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return Category.objects.all()


class CategoryDetailView(APIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get(self, request, slug, id, *args, **kwargs):
        category = get_object_or_404(Category, slug=slug, id=id)
        serializer = self.serializer_class(category, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, slug, *args, **kwargs):
        category = get_object_or_404(Category, slug=slug)
        serializer = self.serializer_class(category)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  
    def delete(self, request, slug, *args, **kwargs):
        category = get_object_or_404(Category, slug=slug)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductsListView(ListAPIView):
    serializer_class = ProductsSerializer
    permission_classes = [AllowAny]
    filterset_class = ProductsFilter  
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter] 
    ordering_fields = ['name', 'price', 'category'] 
    ordering = ['name']  
    search_fields = ['name', 'description']
    pagination_class = ProductsPagination  # Classe de paginação

    def get(self, request, *args, **kwargs):        
        products = self.filter_queryset(self.get_queryset())       
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(products, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):       
        return Products.objects.all()


class ProductDetailView(APIView):
    serializer_class = ProductsSerializer
    permission_classes = [AllowAny]

    def get(self, request, category_slug, category_id, product_slug, product_id, *args, **kwargs):
        category = get_object_or_404(Category, slug=category_slug, id=category_id)
        product = get_object_or_404(Products, slug=product_slug, id=product_id, category=category)
        serializer = self.serializer_class(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, category_slug, category_id, product_slug, product_id, *args, **kwargs):
        # Adiciona ou atualiza um produto no carrinho
        category = get_object_or_404(Category, slug=category_slug, id=category_id)
        product = get_object_or_404(Products, slug=product_slug, id=product_id, category=category)
        
        # Inicializa o carrinho
        cart = Cart(request)

        # Adiciona o produto ao carrinho (quantidade fornecida pela requisição)
        quantity = request.data.get('quantity', 1)
        override_quantity = request.data.get('override_quantity', False)
        cart.add(product=product, quantity=quantity, override_quantity=override_quantity)

        return Response({'message': 'Product added/updated in cart'}, status=status.HTTP_200_OK)

    def delete(self, request, category_slug, category_id, product_slug, product_id, *args, **kwargs):
        # Remove um produto do carrinho
        category = get_object_or_404(Category, slug=category_slug, id=category_id)
        product = get_object_or_404(Products, slug=product_slug, id=product_id, category=category)
        
        # Inicializa o carrinho
        cart = Cart(request)

        # Remove o produto do carrinho
        cart.remove(product=product)

        return Response({'message': 'Product removed from cart'}, status=status.HTTP_204_NO_CONTENT)


class CartDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # Inicializa o carrinho
        cart = Cart(request)
        
        # Itera sobre os produtos no carrinho
        products = []
        for item in cart:
            product = item['product']
            product_data = {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': item['quantity'],
                'total_price': item['total_price']
            }
            products.append(product_data)
        
        # Retorna a lista de produtos com suas quantidades e preços totais
        return Response({'products': products, 'total_price': cart.get_total_price()}, status=200)
