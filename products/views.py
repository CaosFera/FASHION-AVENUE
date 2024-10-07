from django.shortcuts import render, get_object_or_404
from .models import Category, Products
from .serializers import CategorySerializer, ProductsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .filters import CategoryFilter, ProductsFilter
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import CategoryPagination, ProductsPagination
from .cart import Cart
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import PermissionDenied


class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filterset_class = CategoryFilter  
    filter_backends = [DjangoFilterBackend]  
    pagination_class = CategoryPagination

    def get(self, request, *args, **kwargs):
        categories = self.filter_queryset(self.get_queryset())
        
      
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

    def post(self, request, *args, **kwargs):
        # Apenas administradores podem criar categorias
        if not request.user.is_staff:
            raise PermissionDenied("Somente administradores podem criar categorias.")
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, slug, *args, **kwargs):
        
        if not request.user.is_staff:
            raise PermissionDenied("Somente administradores podem editar categorias.")
        category = get_object_or_404(Category, slug=slug)
        serializer = self.serializer_class(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, *args, **kwargs):
        # Apenas administradores podem deletar categorias
        if not request.user.is_staff:
            raise PermissionDenied("Somente administradores podem deletar categorias.")
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
    pagination_class = ProductsPagination  

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

    def post(self, request, category_slug, category_id, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Somente administradores podem adicionar produtos.")
        category = get_object_or_404(Category, slug=category_slug, id=category_id)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(category=category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, category_slug, category_id, product_slug, product_id, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Somente administradores podem editar produtos.")
        category = get_object_or_404(Category, slug=category_slug, id=category_id)
        product = get_object_or_404(Products, slug=product_slug, id=product_id, category=category)
        serializer = self.serializer_class(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_slug, category_id, product_slug, product_id, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Somente administradores podem deletar produtos.")
        category = get_object_or_404(Category, slug=category_slug, id=category_id)
        product = get_object_or_404(Products, slug=product_slug, id=product_id, category=category)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
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

        return Response({'products': products, 'total_price': cart.get_total_price()}, status=200)


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        override_quantity = request.data.get('override_quantity', False)

        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return Response({"error": "Produto não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        cart = Cart(request)
        cart.add(product=product, quantity=quantity, override_quantity=override_quantity)

        return Response({'message': 'Produto adicionado/atualizado no carrinho'}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')

        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return Response({"error": "Produto não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        cart = Cart(request)
        cart.remove(product=product)

        return Response({'message': 'Produto removido do carrinho'}, status=status.HTTP_200_OK)
