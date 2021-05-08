from django.contrib import admin
from .models import TagView, CountryView
# Register your models here.

admin.site.register(TagView)
admin.site.register(CountryView)
