
from django.contrib.auth import get_user_model
from django.db.models import Count

from accounts.models import UserProfile

from django import template

register = template.Library()

User = get_user_model()


@register.inclusion_tag(
    'accounts/snippets/recommended.html'
)
def recommended(user):
    if isinstance(user, User):
        profile = user.profile
        following = profile.get_following()
        print(following)
        qs = User.objects.all()\
            .annotate(num_posts=Count('post'))\
            .annotate(num_likes=Count('post__likes'))\
            .order_by('-num_likes', '-num_posts')\
            .exclude(id=profile.id)\
            .exclude(id__in=following)
        print(qs)
        return {"recommended": qs}

