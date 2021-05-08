from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
)

from analytics.models import TagView
from .models import Tag
# Create your views here.


class TagDetailView(DetailView):
    model = Tag

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            tag = self.get_object()
            new_view_tag = TagView.objects.add_count(
                self.request.user, tag
            )
        return context


class TagListView(ListView):
    model = Tag

    def get_queryset(self):
        return Tag.objects.all()

