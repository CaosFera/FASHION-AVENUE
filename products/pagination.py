from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class CategoryPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

class ProductsPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'  
    max_page_size = 20