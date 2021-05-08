from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class ProductManager(models.Manager):
    def add_count(self, user, post):
        obj, created = self.model.objects.get_or_create(
            user=user,
            post=post
        )
        obj.count = obj.count_likes.count()
        obj.save()
        return obj

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=2000)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blog_posts')

    def __str__(self):
        return f"{self.id}"

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = [
            '-timestamp'
        ]
