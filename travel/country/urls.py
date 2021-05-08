from django.urls import path
from .views import (
    CountryListView,
    CountryDetailView
)
app_name = "country"
urlpatterns = [
    path('', CountryListView.as_view(), name="list"),
    path('<slug:slug>/', CountryDetailView.as_view(), name="detail"),
]
