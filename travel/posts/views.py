from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView
)
from django.views.generic.base import View

from analytics.models import TagView, CountryView
from country.models import Country
from tags.models import Tag
from .forms import PostModelForm
from .mixins import FormUserMixin, UserOwnerMixin
from .models import Post


class PostCreateView(FormUserMixin, CreateView):
    form_class = PostModelForm
    template_name = "posts/post_create.html"

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        valid_data = super(PostCreateView, self).form_valid(form)
        tags = form.cleaned_data.get("tags")
        country = form.cleaned_data.get("countries")
        if tags:
            tags_list = tags.split(',')
            for tag in tags_list:
                if not tag == " ":
                    new_tag = Tag.objects.get_or_create(
                        title=str(tag).strip())[0]
                    new_tag.posts.add(form.instance)
        if country:
            new_country = Country.objects.get_or_create(
                title=str(country).strip())[0]
            new_country.posts.add(form.instance)

        return valid_data


class PostUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    queryset = Post.objects.all()
    form_class = PostModelForm
    template_name = "posts/post_update.html"

    def get_initial(self):
        initial = super(PostUpdateView, self).get_initial()
        tags = self.get_object().tag_set.all()
        initial['tags'] = ", ".join([x.title for x in tags])
        return initial

    def form_valid(self, form):
        valid_data = super(PostUpdateView, self).form_valid(form)
        tags = form.cleaned_data.get("tags")
        country = form.cleaned_data.get("countries")
        obj = self.get_object()
        obj.tag_set.clear()
        obj.country_set.clear()
        if tags:
            tags_list = tags.split(',')
            for tag in tags_list:
                if not tag == " ":
                    new_tag = \
                    Tag.objects.get_or_create(title=str(tag).strip())[0]
                    new_tag.posts.add(self.get_object())
        if country:
            new_country = Country.objects.get_or_create(
                title=str(country).strip())[0]
            new_country.posts.add(form.instance)
        return valid_data


class PostDetailView(DetailView):
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['total_likes'] = total_likes
        context['liked'] = liked
        obj = self.get_object()
        tags = obj.tag_set.all()
        countries = obj.country_set.all()
        for tag in tags:
            new_view_tag = TagView.objects.add_count(
                self.request.user, tag
            )
        for country in countries:
            new_view_country = CountryView.objects.add_count(
                self.request.user, country
            )
        return context


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('posts:detail', args=[str(pk)]))


class PostListView(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Post

    def get_queryset(self, *args, **kwargs):
        qs = Post.objects.all()
        # im_following = self.request.user.profile.get_following()
        # qs1 = Post.objects.filter(user__in=im_following)
        # qs2 = Post.objects.filter(user=self.request.user)
        # qs = (qs1 | qs2).distinct().order_by("-timestamp")
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(user__username__icontains=query)
            )
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = PostModelForm
        context["create_url"] = reverse_lazy("posts:create")
        return context


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "posts/post_delete.html"
    success_url = reverse_lazy("posts:list")


