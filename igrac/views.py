from django.views.generic import TemplateView, ListView
from geonode.maps.models import Map


class HomeView(ListView):
    model = Map
    paginate_by = 100
    template_name = 'landing_page.html'
    context_object_name = 'maps'
