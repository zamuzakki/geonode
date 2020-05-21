from geonode.groups.models import Group, GroupProfile


def set_default_filter_by_group(sender, request, user, **kwargs):
    """
    Set layer/map/document to be filtered by user's group by default
    """

    groups = GroupProfile.objects.filter(
        group__in=request.user.groups.exclude(name='anonymous')
    ).values_list('slug',flat = True)

    filter = ""
    for group in groups:
        filter = filter + "&" + "group__group_profile__slug__in=" + group

    request.session['filter_by_group'] = filter