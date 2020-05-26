# coding=utf-8
"""Urls for igrac apps."""

from django.conf.urls import url
from .views import HomeView, map_view_with_slug

urlpatterns = [
    url(r'^$',
        view=HomeView.as_view(),
        name='home_igrac'),
    url(r'^maps/view/(?P<slug>[^/]+)$',
        view=map_view_with_slug,
        name='map_view_slug'),
]
