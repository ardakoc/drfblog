from django.db import models
from django.contrib.auth.models import User

from post.models import Post


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.user.username + ' ' + self.post.title