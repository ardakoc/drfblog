from rest_framework import serializers

from django.contrib.auth.models import User

from comment.models import Comment
from post.models import Post


class CommentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class CommentPostSerializer(serializers.ModelSerializer):
    user = CommentUserSerializer()

    class Meta:
        model = Post
        fields = ['id', 'title', 'user']


class CommentBaseSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user = CommentUserSerializer()
    post = CommentPostSerializer()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_replies(self, obj):
        if obj.any_children:
            return CommentBaseSerializer(obj.children(), many=True).data
        

class CommentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['content', ]


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

    # def validate(self, attrs):
    #     if attrs['parent']:
    #         if attrs['parent'].post != attrs['post']:
    #             raise serializers.ValidationError(
    #                 'Selected post does not match with parent\'s post.')
    #     return attrs
    
    # def create(self, validated_data):
    #     comment = Comment.objects.create(**validated_data)
    #     return comment
