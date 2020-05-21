from django.db import models
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .signals import set_default_filter_by_group as filter_by_group_signals

# Create your models here.

@receiver(user_logged_in)
def set_default_filter_by_group(sender, request, user, **kwargs):
    """
    Set layer/map/document to be filtered by user's group by default
    """
    filter_by_group_signals(sender, request, user, **kwargs)
