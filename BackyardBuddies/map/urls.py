from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='map-home'),
    path("feed/", views.feed, name='map-feed'),
]
