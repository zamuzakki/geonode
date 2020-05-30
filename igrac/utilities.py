# coding=utf-8
from geonode.groups.models import Group, GroupProfile
from geonode.maps.models import Map
from geonode.documents.models import Document
from geonode.layers.models import Layer

STOP_WORDS = (
    'a', 'an', 'and', 'if', 'is', 'the', 'in', 'i', 'you', 'other',
    'this', 'that', 'to',
)


def check_slug(queryset, slug):
    """
    This function checks slug within a model queryset
    and return a new incremented slug when there are duplicates.

    """

    registered_slug = queryset.values_list('slug', flat=True)
    new_slug = slug
    if slug in registered_slug:
        match_slug = [s for s in registered_slug if slug in s]
        num = len(match_slug)
        num_char = 50 - (len(str(num)) + 1)
        new_slug = slug[:num_char] + '-' + str(num)

    return new_slug

def get_default_filter_by_group(user, type='layer'):
    """
    Set layer/map/document filter by user's group by default
    """
    user_groups = GroupProfile.objects.filter(
        group__in=user.groups.exclude(name='anonymous')
    )
    # values_list('slug', flat=True)

    if type == 'layer':
        obj_groups = GroupProfile.objects.filter(
            group__id__in=Layer.objects.values_list('group__id', flat=True)
        )
    if type == 'map':
        obj_groups = GroupProfile.objects.filter(
            group__id__in=Map.objects.values_list('group__id', flat=True)
        )
    if type == 'document':
        obj_groups = GroupProfile.objects.filter(
            group__id__in=Document.objects.values_list('group__id', flat=True)
        )
    groups = obj_groups.intersection(user_groups).values_list('slug', flat=True)

    filter = ""
    for group in groups:
        filter = filter + "&" + "group__group_profile__slug__in=" + group

    return filter
