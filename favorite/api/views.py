from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import redirect

from favorite.models import Favorite
from favorite.api.serializers import FavoriteSerializer
from favorite.api.permissions import IsOwner
from post.models import Post


class PostListFavoriteCreateAPIView(APIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, ]
    throttle_scope = 'favorite'

    def post(self, request):
        post = Post.objects.get(id=request.POST.get('fav-post'))
        Favorite.objects.create(user=request.user, post=post)
        return redirect('post:post_list')
    

class PostListFavoriteDeleteAPIView(APIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsOwner, ]

    def post(self, request):
        post = Post.objects.get(id=request.POST.get('delete-fav-post'))
        Favorite.objects.filter(user=request.user, post=post).delete()
        return redirect('post:post_list')
    

class PostDetailFavoriteCreateAPIView(APIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, ]
    throttle_scope = 'favorite'

    def post(self, request):
        post = Post.objects.get(slug=request.POST.get('fav-post'))
        Favorite.objects.create(user=request.user, post=post)
        return redirect('post:post_detail', slug=request.POST.get('fav-post'))
    

class PostDetailFavoriteDeleteAPIView(APIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsOwner, ]

    def post(self, request):
        post = Post.objects.get(slug=request.POST.get('delete-fav-post'))
        Favorite.objects.filter(user=request.user, post=post).delete()
        return redirect(
            'post:post_detail', slug=request.POST.get('delete-fav-post'))    


class ProfilePageFavoriteCreateAPIView(APIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, ]
    throttle_scope = 'favorite'

    def post(self, request):
        post = Post.objects.get(slug=request.POST.get('fav-post'))
        Favorite.objects.create(user=request.user, post=post)
        return redirect('account:profile')
    

class ProfilePageFavoriteDeleteAPIView(APIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsOwner, ]

    def post(self, request):
        post = Post.objects.get(slug=request.POST.get('delete-fav-post'))
        Favorite.objects.filter(user=request.user, post=post).delete()
        return redirect('account:profile')
