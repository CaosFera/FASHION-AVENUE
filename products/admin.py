from django.contrib import admin
from .models import Category, Products




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'active', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('name', 'active', 'created_at')
    ordering = ('name', 'created_at')  
    exclude = ('slug',) 

     

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'active', 'created_at', 'updated_at', 'size', 'color', 'description')
    search_fields = ('name', 'price', 'stock', 'category', 'active', 'created_at', 'updated_at', 'size', 'color')
    list_filter = ('category','name', 'created_at', 'color', 'size')
    ordering = ('name', 'category', '-created_at')  
    exclude = ('slug',) 
