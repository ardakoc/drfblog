from django.urls import path

from favorite.api import views


app_name = 'favorite'

urlpatterns = [
    path('create-pl/', views.PostListFavoriteCreateAPIView.as_view(), name='create-pl'),
    path('delete-pl/', views.PostListFavoriteDeleteAPIView.as_view(), name='delete-pl'),
    path('create-pd/', views.PostDetailFavoriteCreateAPIView.as_view(), name='create-pd'),
    path('delete-pd/', views.PostDetailFavoriteDeleteAPIView.as_view(), name='delete-pd'),
    path('create-pp/', views.ProfilePageFavoriteCreateAPIView.as_view(), name='create-pp'),
    path('delete-pp/', views.ProfilePageFavoriteDeleteAPIView.as_view(), name='delete-pp'),
]