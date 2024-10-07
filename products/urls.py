from django.urls import path
from .views import CategoryListView, CategoryDetailView, ProductsListView, ProductDetailView
from .views import CartView, CartDetailView


urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),  
    path('category/<slug:slug>/<int:id>/', CategoryDetailView.as_view(), name='category-detail'),  
    path('products/', ProductsListView.as_view(), name='products-list'),  
    path('category/<slug:category_slug>/<int:category_id>/product/<slug:product_slug>/<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart-detail/', CartDetailView.as_view(), name='cart-detail'),
    
]
