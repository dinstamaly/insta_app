from django.db import models

# Create your models here.
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify

from posts.models import Post


class TagQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)


class TagManager(models.Manager):
    def get_queryset(self):
        return TagQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return super(TagManager, self).all(*args, **kwargs).filter(active=True)


class Tag(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    posts = models.ManyToManyField(Post, blank=True)
    active = models.BooleanField(default=True)

    objects = TagManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("tags:detail", kwargs={"slug": self.slug})


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


pre_save.connect(tag_pre_save_receiver, sender=Tag)

