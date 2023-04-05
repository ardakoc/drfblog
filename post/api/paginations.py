from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator


class PostPagination(PageNumberPagination, Paginator):
    page_size = 4
    template = 'html/post/post_list.html'
