from django.shortcuts import redirect
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, \
                        CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User

from account.api.serializers import UserSerializer, ChangePasswordSerializer,\
                        RegisterSerializer
from account.api.permissions import IsNotAuthenticated
from account.api.throttles import RegisterThrottle

from post.models import Post
from post.api.paginations import PostPagination
from post.api.serializers import PostSerializer
from favorite.models import Favorite


class ProfileAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]
    renderer_classes = [TemplateHTMLRenderer, ]
    template_name = 'html/account/profile.html'

    def get_queryset(self):
        return User.objects.all()

    def get(self, request):
        user = get_object_or_404(User, id=self.request.user.id)
        posts = Post.objects.filter(user=user)
        favorites = Favorite.objects.filter(user=request.user)
        favorite_posts = []
        for favorite in favorites:
            favorite_posts.append(favorite.post)
        return Response(
            {'user': user, 'posts': posts, 'favorites': favorite_posts})
    

class ProfileUpdateAPIView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]
    renderer_classes = [TemplateHTMLRenderer, ]
    template_name = 'html/account/profile.html'

    def get(self, request):
        user = get_object_or_404(User, id=self.request.user.id)
        posts = Post.objects.filter(user=user)
        favorites = Favorite.objects.filter(user=request.user)
        favorite_posts = []
        for favorite in favorites:
            favorite_posts.append(favorite.post)
        serializer = UserSerializer(user,)
        return Response({
            'serializer': serializer,
            'user': user,
            'posts': posts,
            'favorites': favorite_posts})

    def post(self, request):
        user = get_object_or_404(User, id=self.request.user.id)
        serializer = UserSerializer(user, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'user': user})
        serializer.save()
        return redirect('account:profile')
    

class ProfilePostsRetrieveAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    renderer_classes = [TemplateHTMLRenderer, ]
    template_name = 'html/post/post_list.html'

    def get(self, request):
        user = get_object_or_404(User, id=self.request.user.id)
        posts = Post.objects.filter(user=user)
        paginator = PostPagination(posts, 4)
        queryset = paginator.paginate_queryset(posts, request, view=self)
        serializer = PostSerializer(
            queryset, many=True, context={'request': request})
        response = paginator.get_paginated_response(serializer.data)
        page = paginator.page
        elided_pages = paginator.get_elided_page_range(
            number=page.number, on_each_side=1, on_ends=2)
        favorites = Favorite.objects.filter(user=request.user)
        favorite_posts = []
        for favorite in favorites:
            favorite_posts.append(favorite.post.id)
        return Response({
            'response': response.data,
            'user': user,
            'page': page,
            'elided_pages': elided_pages,
            'favorites': favorite_posts })
    

class ProfileFavoritesRetrieveAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    renderer_classes = [TemplateHTMLRenderer, ]
    template_name = 'html/post/post_list.html'

    def get(self, request):
        user = get_object_or_404(User, id=self.request.user.id)
        posts = Post.objects.all()
        favorites = Favorite.objects.filter(user=request.user)
        user_posts = []
        for fav in favorites:
            if fav.post in posts:
                user_posts.append(fav.post)
        paginator = PostPagination(user_posts, 4)
        queryset = paginator.paginate_queryset(user_posts, request, view=self)
        serializer = PostSerializer(
            queryset, many=True, context={'request': request})
        response = paginator.get_paginated_response(serializer.data)
        page = paginator.page
        elided_pages = paginator.get_elided_page_range(
            number=page.number, on_each_side=1, on_ends=2)
        favorite_posts = []
        for favorite in favorites:
            favorite_posts.append(favorite.post.id)
        return Response({
            'response': response.data,
            'user': user,
            'page': page,
            'elided_pages': elided_pages,
            'favorites': favorite_posts })
    

class UpdatePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    
    def put(self, request, *args, **kwargs):
        self.object = self.request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get('old_password')
            if not self.object.check_password(old_password):
                return Response(
                    {'old_password': 'Wrong password'},
                    status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            update_session_auth_hash(request, self.object)
            return Response(status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CreateUserAPIView(CreateAPIView):
    model = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsNotAuthenticated, ]
    throttle_classes = [RegisterThrottle, ]
