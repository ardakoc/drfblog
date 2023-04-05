from django.urls import path

from post.api import views


app_name = 'post'

urlpatterns = [
    path('list/', views.PostListAPIView.as_view(), name='post_list'),
    path('<slug>/detail/', views.PostDetailAPIView.as_view(), name='post_detail'),
    path(
        '<slug>/update/',
        views.PostUpdateAPIView.as_view(),
        name='post_update'),
    path(
        '<slug>/delete/',
        views.PostDeleteAPIView.as_view(),
        name='post_delete'),
    path(
        'create/',
        views.PostCreateAPIView.as_view(),
        name='post_create'),
]
