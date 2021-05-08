from django.contrib.auth import get_user_model

from django import template
from django.db.models import Count

from posts.models import Post

register = template.Library()

User = get_user_model()


@register.inclusion_tag(
    'posts/snippets/rec_posts.html'
)
def rec_posts(user):
    if isinstance(user, User):
        posts = Post.objects.annotate(q_count=Count('likes'))\
                    .order_by('-q_count')[:5]
        return {"posts": posts}
