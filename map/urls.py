from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path("", views.home, name='map-home'),
    path("feed/", PostListView.as_view(), name='map-feed'),
    path("user/<str:username>", UserPostListView.as_view(), name='user-posts'),
    path("post/<int:pk>/", PostDetailView.as_view(), name='post-detail'),
    path("post/new/", PostCreateView.as_view(), name='post-create'),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name='post-update'),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name='post-delete'),
    path("house/<slug:slug>/", HouseDetailView.as_view(), name='house-detail'),
    path("house/<slug:slug>/update/", HouseUpdateView.as_view(), name='house-update'),
    path("house/<slug:slug>/delete/", HouseDeleteView.as_view(), name='house-delete'),
    path("new_house/", HouseCreateView.as_view(), name='house-create'),
    path('likes/', likes, name='likes'),
]