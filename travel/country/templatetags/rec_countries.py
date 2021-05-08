from django.contrib.auth import get_user_model

from django import template

from analytics.models import CountryView

register = template.Library()

User = get_user_model()


@register.inclusion_tag(
    'country/snippets/rec_countries.html'
)
def rec_countries(user):
    if isinstance(user, User):
        country_views = None
        country_tags = None
        try:
            country_views = CountryView.objects.all().order_by("-count")[:5]
        except:
            pass
        if country_views:
            country_tags = [x.country for x in country_views]
        return {"top_countries": country_tags}
