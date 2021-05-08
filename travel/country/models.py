from django.db import models
# Create your models here.
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify

from posts.models import Post


class CountryManager(models.Manager):
    def all(self, *args, **kwargs):
        return super(CountryManager, self).all(*args, **kwargs).filter(
            active=True)


class Country(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    posts = models.ManyToManyField(Post, blank=True)
    active = models.BooleanField(default=True)

    objects = CountryManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("country:detail", kwargs={"slug": self.slug})


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Country.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(product_pre_save_receiver, sender=Country)
