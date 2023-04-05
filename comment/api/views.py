from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.generics import ListAPIView, RetrieveAPIView,\
                            RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import DestroyModelMixin

from django.shortcuts import get_object_or_404, redirect

from comment.models import Comment
from comment.api.serializers import CommentBaseSerializer,\
                            CommentUpdateSerializer, CommentCreateSerializer
from comment.api.permissions import IsOwnerOrSuperuser
from comment.api.pagination import CommentPagination
from post.models import Post


class CommentListAPIView(ListAPIView):
    serializer_class = CommentBaseSerializer
    pagination_class = CommentPagination

    def get_queryset(self):
        queryset = Comment.objects.filter(parent=None)
        query = self.request.GET.get('postid')
        
        if query:
            queryset = queryset.filter(post=query)

        return queryset


class CommentDetailAPIView(RetrieveAPIView):
    serializer_class = CommentBaseSerializer

    def get_queryset(self):
        return Comment.objects.all()
    

class CommentUpdateAPIView(APIView):
    serializer_class = CommentUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSuperuser, ]
    throttle_scope = 'comment'

    def get_queryset(self):
        return Comment.objects.all()
    
    # def put(self, request, *args, **kwargs):



class CommentDeleteAPIView(APIView):
    serializer_class = CommentUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSuperuser, ]
    throttle_scope = 'comment'

    def get_queryset(self):
        return Comment.objects.all()
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CommentCreateAPIView(APIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated, ]
    throttle_scope = 'comment'

    def get_queryset(self):
        return Comment.objects.all()

    def post(self, request):
        if request.method == 'POST':
            user = self.request.user
            slug = request.POST.get('comment-post')
            post = Post.objects.get(slug=slug)
            content = request.POST.get('comment-content')
            comment = Comment(content=content, user=user, post=post)
            comment.save()
        return HttpResponseRedirect(reverse('post:post_detail', args=[slug]))
