import os
import requests


def get_countries():
    url = 'https://restcountries.eu/rest/v2/all'
    r = requests.get(url)
    countries = r.json()
    country_list = []
    length = len(countries)

    for i in range(length):
        country_list.append(countries[i]['name'])
    return country_list


def get_country(name):
    url = 'https://restcountries.eu/rest/v2/alpha/%s' % name
    r = requests.get(url)
    country = r.json()
    return country
