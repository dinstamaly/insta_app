from django.db.models import Q
from rest_framework import generics
from rest_framework import permissions
from posts.models import Post
from .pagination import StandardResultsPagination
from .serializers import PostModelSerializer


class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostListAPIView(generics.ListAPIView):
    serializer_class = PostModelSerializer
    pagination_class = StandardResultsPagination

    def get_queryset(self, *args, **kwargs):
        im_following = self.request.user.profile.get_following()
        qs1 = Post.objects.filter(user__in=im_following)
        qs2 = Post.objects.filter(user=self.request.user)
        qs = (qs1 | qs2).distinct().order_by("-timestamp")
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(user__username__icontains=query)
            )

        return qs


