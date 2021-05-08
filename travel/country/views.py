import requests
from django.views.generic import (
    ListView,
    DetailView,
)

from analytics.models import CountryView
from .models import Country
# Create your views here.


class CountryDetailView(DetailView):
    model = Country

    def get_context_data(self, **kwargs):
        context = super(CountryDetailView, self).get_context_data(**kwargs)
        country = self.get_object()
        url = 'https://restcountries.eu/rest/v2/name/%s' % country

        response = requests.get(url)
        data = response.json()[0]
        context['currency'] = data['currencies'][0]['name']
        context['currency_symbol'] = data['currencies'][0]['symbol']
        context['country_flag'] = data['flag']
        context['country_lang'] = [x['name'] for x in data['languages']]
        context['country_cap'] = data['capital']
        context['country_region'] = data['region']

        if self.request.user.is_authenticated:
            new_view_country = CountryView.objects.add_count(
                self.request.user, country
            )
        return context


class CountryListView(ListView):
    model = Country

    def get_queryset(self):
        return Country.objects.all()


