from django.conf import settings
from django.db import models

from tags.models import Tag
from country.models import Country


class TagViewManager(models.Manager):
    def add_count(self, user, tag):
        obj, created = self.model.objects.get_or_create(
            user=user,
            tag=tag
        )
        obj.count += 1
        obj.save()
        return obj


class TagView(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True, null=True, on_delete=models.SET_NULL
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    objects = TagViewManager()

    def __str__(self):
        return self.tag.title


class CountryViewManager(models.Manager):
    def add_count(self, user, country):
        obj, created = self.model.objects.get_or_create(
            user=user,
            country=country
        )
        obj.count += 1
        obj.save()
        return obj


class CountryView(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True, null=True,
        on_delete=models.SET_NULL
    )
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

    objects = CountryViewManager()

    def __str__(self):
        return self.country.title
