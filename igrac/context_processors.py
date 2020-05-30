from .utilities import get_default_filter_by_group

def resource_urls(request):
    """Global values to pass to templates"""

    defaults = dict(
        MAP_DEFAULT_FILTER=get_default_filter_by_group(request.user, type="map"),
        LAYER_DEFAULT_FILTER=get_default_filter_by_group(request.user, type="layer"),
        DOCUMENT_DEFAULT_FILTER=get_default_filter_by_group(request.user, type="document"),
    )

    return defaults
