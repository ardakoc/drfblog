from django.urls import path

from account.api import views


app_name = 'account'

urlpatterns = [
    path('profile/', views.ProfileAPIView.as_view(), name='profile'),
    path(
        'profile/update/',
        views.ProfileUpdateAPIView.as_view(),
        name='profile_update'),
    path(
        'profile/posts/',
        views.ProfilePostsRetrieveAPIView.as_view(),
        name='profile_posts'),
    path(
        'profile/favorites/',
        views.ProfileFavoritesRetrieveAPIView.as_view(),
        name='profile_favorites'),
    path(
        'change-password/',
        views.UpdatePasswordAPIView.as_view(),
        name='change-password'),
    path('register/', views.CreateUserAPIView.as_view(), name='register'),
]
