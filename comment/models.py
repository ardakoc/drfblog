from django.db import models
from django.contrib.auth.models import User

from post.models import Post


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return self.post.title + ' ' + self.user.username
    
    def children(self):
        return Comment.objects.filter(parent=self)
    
    @property
    def any_children(self):
        return Comment.objects.filter(parent=self).exists()
    
    
