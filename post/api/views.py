from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator

from post.models import Post
from post.api.serializers import PostSerializer, PostCreateSerializer, \
                                 PostUpdateSerializer
from post.api.permissions import IsAuthorOrSuperuser
from post.api.paginations import PostPagination
from favorite.models import Favorite
from comment.api.views import CommentListAPIView
from comment.models import Comment


class PostListAPIView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny, ]
    filter_backends = [SearchFilter, OrderingFilter ,]
    search_fields = ['title', 'content']
    renderer_classes = [TemplateHTMLRenderer, ]
    template_name = 'html/post/post_list.html'

    def get_queryset(self):
        return Post.objects.all()

    def get(self, request):
        posts = self.get_queryset()
        paginator = PostPagination(posts, 4)
        queryset = paginator.paginate_queryset(posts, request, view=self)
        serializer = PostSerializer(
            queryset, many=True, context={'request': request})
        response = paginator.get_paginated_response(serializer.data)
        page = paginator.page
        elided_pages = paginator.get_elided_page_range(
            number=page.number, on_each_side=1, on_ends=2)
        if request.user.is_authenticated:
            favorites = Favorite.objects.filter(user=request.user)
            favorite_posts = []
            for favorite in favorites:
                favorite_posts.append(favorite.post.id)
            context = {
                'response': response.data,
                'page': page,
                'elided_pages': elided_pages,
                'favorites': favorite_posts }
        else:
            context = {
                'response': response.data,
                'page': page,
                'elided_pages': elided_pages }
        return Response(context)
        

class PostDetailAPIView(RetrieveAPIView):
    serializer_class = PostSerializer
    lookup_field = 'slug'
    renderer_classes = [TemplateHTMLRenderer, ]
    template_name = 'html/post/post_detail.html'

    def get_queryset(self):
        return Post.objects.all()

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        comments = Comment.objects.filter(post=post)
        if request.user.is_authenticated:
            try:
                favorite = Favorite.objects.get(
                    user=request.user, post=post)
            except:
                favorite = None
            return Response({
                'post': post,
                'favorite': favorite,
                'comments': comments})
        return Response({'post': post})


class PostCreateAPIView(APIView):
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated, ]
    throttle_scope = 'post'
    renderer_classes = [TemplateHTMLRenderer, ]
    template_name = 'html/post/post_create.html'

    def get_queryset(self):
        return Post.objects.all()

    def get(self, request):
        serializer = PostSerializer()
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer})
        serializer.save(user=self.request.user)
        return redirect('post:post_create')


class PostUpdateAPIView(APIView):
    serializer_class = PostUpdateSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated, IsAuthorOrSuperuser, ]
    throttle_scope = 'post'
    renderer_classes = [TemplateHTMLRenderer, ]
    template_name = 'html/post/post_update.html'

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        serializer_context = {'request': request}
        serializer = PostSerializer(post, context=serializer_context)
        return Response({'serializer': serializer, 'post': post})

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        serializer = PostUpdateSerializer(post, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'post': post})
        serializer.save()
        return redirect('post:post_list')
    

class PostDeleteAPIView(APIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated, IsAuthorOrSuperuser, ]
    throttle_scope = 'post'
    renderer_classes = [TemplateHTMLRenderer, ]
    template_name = 'html/post/post_delete.html'

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        serializer_context = {'request': request}
        serializer = PostSerializer(post, context=serializer_context)
        return Response({'serializer': serializer, 'post': post})
    
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        post.delete()
        return redirect('post:post_list')
