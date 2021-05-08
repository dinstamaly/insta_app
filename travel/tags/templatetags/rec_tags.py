from django.contrib.auth import get_user_model

from accounts.models import UserProfile

from django import template

from analytics.models import TagView

register = template.Library()

User = get_user_model()


@register.inclusion_tag(
    'tags/snippets/rec_tags.html'
)
def rec_tags(user):
    if isinstance(user, User):
        tag_views = None
        top_tags = None
        try:
            tag_views = TagView.objects.all().order_by("-count")[:5]
        except:
            pass
        if tag_views:
            top_tags = [x.tag for x in tag_views]
        return {"top_tags": top_tags}
