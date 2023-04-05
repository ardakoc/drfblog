from rest_framework import serializers

from post.models import Post


class PostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name = 'post:post_detail',
        lookup_field = 'slug',
    )

    author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        exclude = ['slug']

    def get_author(self, obj):
        return obj.user.username
    
    def to_representation(self, instance):
        representation = super(PostSerializer, self).to_representation(instance)
        representation['created'] = instance.created.strftime('%d-%m-%Y - %H:%M')
        return representation
    
    
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'draft', 'image']
    
    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        return post


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'draft', 'image']
    