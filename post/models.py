from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    title = models.CharField(max_length=120)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=150, editable=False, default=None)
    image = models.ImageField(upload_to='post/', null=True, blank=True)

    class Meta:
        ordering = ['-id', ]

    def __str__(self):
        return self.title

    def get_slug(self):
        slug = slugify(self.title.replace('ı','i'))
        unique = slug
        number = 1

        while Post.objects.filter(slug=unique).exists():
            unique = f'{slug}-{number}'
            number += 1

        return unique

    def save(self, *args, **kwargs):
        self.slug = self.get_slug()
        return super(Post, self).save(*args, **kwargs)
    