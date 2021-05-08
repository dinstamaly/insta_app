from django.views.generic import RedirectView
from django.urls import path
from .views import (
    PostListAPIView,
    PostCreateAPIView
)
app_name = "posts-api"
urlpatterns = [
    # path('', RedirectView.as_view(url="")),
    path('', PostListAPIView.as_view(), name="list"),
    path('create/', PostCreateAPIView.as_view(), name="create"),
    # path('<int:pk>/', PostDetailView.as_view(), name="detail"),
    # path('<int:pk>/edit/', PostUpdateView.as_view(), name="edit"),
    # path('<int:pk>/delete/', PostDeleteView.as_view(), name="delete"),
]
