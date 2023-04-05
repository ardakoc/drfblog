from rest_framework import pagination


class CommentPagination(pagination.PageNumberPagination):
    page_size = 4