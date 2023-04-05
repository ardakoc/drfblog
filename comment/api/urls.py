from django.urls import path

from comment.api import views


app_name = 'comment'

urlpatterns = [
    path('list/', views.CommentListAPIView.as_view(), name='comment_list'),
    path('<pk>/detail/', views.CommentDetailAPIView.as_view(), name='comment_detail'),
    path(
        '<pk>/update/',
        views.CommentUpdateAPIView.as_view(),
        name='comment_update'),
    path(
        '<pk>/delete/',
        views.CommentDeleteAPIView.as_view(),
        name='comment_delete'),
    path(
        'create/',
        views.CommentCreateAPIView.as_view(),
        name='comment_create'),
]
