import logging
from django.test import TestCase
from django.urls import reverse
from geonode.base.populate_test_data import create_models
from geonode.maps.models import Map
from igrac.models.map_slug import MapSlugMapping

logger = logging.getLogger(__name__)

class MapSlugTest(TestCase):
    def setUp(self):
        self.object_ids = create_models()

    def test_map_slug_auto_creation(self):
        """
        Map Slugs should be automatically created, and the number
        is equal to created Map.
        :return:
        """
        map_slugs = MapSlugMapping.objects.all()
        self.assertEqual(len(self.object_ids), map_slugs.count())

    def test_map_slug_auto_deletion(self):
        """
        Map Slugs should be automatically deleted after Map deletion
        :return:
        """
        Map.objects.get(self.object_ids[0]).delete()
        map_slug = MapSlugMapping.objects.filter(map__id=self.object_ids[0])
        self.assertEqual(map_slug.count(), 0)