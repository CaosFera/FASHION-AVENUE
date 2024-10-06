from django_filters import rest_framework as filters
from .models import Category, Products
from django.db import models
from django.db.models import Q


class CategoryFilter(filters.FilterSet):
    name  = filters.ModelChoiceFilter(queryset=Category.objects.all(), label='Categoria')
    
    class Meta:
        model = Category
        fields = ['name']
        
class ProductsFilter(filters.FilterSet):
    SIZE_CHOICES = [
        ('Pequeno', 'Pequeno'),
        ('Médio', 'Médio'),
        ('Grande', 'Grande'),
        ('Extra-Grande', 'Extra-Grande'),
    ]
    COLOR_CHOICES = [
        ('Vermelho', 'Vermelho'),
        ('Verde', 'Verde'),
        ('Azul', 'Azul'),
        ('Branco', 'Branco'),
        ('Preto', 'Preto'),
        ('Rosa', 'Rosa'),
        ('Laranja', 'Laranja'),
        ('Marron', 'Marron'),
    ]
    
    color = filters.ChoiceFilter(field_name="color", choices=COLOR_CHOICES, label='Cor')
    size = filters.ChoiceFilter(field_name="size", choices=SIZE_CHOICES, label='Tamanho')
    category = filters.ModelChoiceFilter(queryset=Category.objects.all(), label='Categoria')
    price = filters.NumberFilter(field_name='price', lookup_expr='lte', label='Preço')
    

    class Meta:
        model = Products
        fields = ['color', 'size', 'price', 'category']
    
   