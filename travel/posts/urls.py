from django.views.generic import RedirectView
from django.urls import path
from .views import (
    PostDetailView,
    PostListView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    LikeView
)
app_name = "posts"
urlpatterns = [
    path('', RedirectView.as_view(url="")),
    path('search/', PostListView.as_view(), name="list"),
    path('create/', PostCreateView.as_view(), name="create"),
    path('<int:pk>/', PostDetailView.as_view(), name="detail"),
    path('like/<int:pk>/', LikeView, name="like_post"),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name="edit"),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name="delete"),
]
