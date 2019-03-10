import json
from collections import Counter
from pprint import pprint

from django.contrib.gis.geos import Point, GEOSGeometry, Polygon, LineString
from django.core.management.base import BaseCommand

from core.models import Place

REST_URL = "http://overpass-api.de/api/interpreter"
# ?data=
REST_PARAM = """[out:json][timeout:500];area(3601473946)->.a;area(3601703814)->.b;(node["place"]["name"](area.a);node["historic"]["name"](area.a);node["natural"]["name"](area.a);node["place"]["name"](area.b);node["historic"]["name"](area.b);node["natural"]["name"](area.b);way["waterway"]["name"](area.a);way["waterway"]["name"](area.b););out;"""

GEOJSON = "places.geojson"
GEOJSON = "take3.geojson"
GEOJSON = "waterways.geojson"


class Command(BaseCommand):
    help = "Import places from csv file"

    def handle(self, *args, **options):
        c = Counter()
        with open(GEOJSON) as f:
            features = json.load(f)['features']
        total = len(features)
        print(total)

        try:
            for i, ft in enumerate(features, 1):
                if i % 250 == 0:
                    print(i, total)
                p = ft['properties']
                g = p.get
                name = g('name:he', g('name'))
                if not name:
                    print(i, "NO NAME", ft['id'])
                    c['noname'] += 1
                    continue
                geom = GEOSGeometry(json.dumps(ft['geometry']))
                t = geom.__class__.__name__
                if isinstance(geom, Polygon):
                    geom = geom.centroid
                elif isinstance(geom, LineString):
                    geom = geom.centroid
                elif isinstance(geom, Point):
                    pass
                else:
                    assert False, geom
                p, created = Place.objects.update_or_create(
                    osm_id=ft['id'],
                    defaults=dict(
                        name=name,
                        geom=geom,
                        raw_data=ft,
                    )
                )
                c[f"{t}.{'created' if created else 'updated'}"] += 1
        finally:
            pprint(dict(c))
