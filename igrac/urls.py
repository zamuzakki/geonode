# coding=utf-8
"""Urls for igrac apps."""

from django.conf.urls import url
from .views import HomeView

urlpatterns = [
    url(r'^$',
        view=HomeView.as_view(),
        name='home_igrac'),
]
