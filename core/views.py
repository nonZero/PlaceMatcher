import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.geos import Point
from django.db import transaction
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView

from core.models import Photo, Suggestion, Place


class PhotoListView(LoginRequiredMixin, ListView):
    model = Photo
    paginate_by = 25
    ordering = "?"


class PhotoDetailView(LoginRequiredMixin, DetailView):
    model = Photo

    def app_data(self):
        o: Photo = self.get_object()
        return {
            'id': o.id,
            'place': o.selected_place and {
                'id': o.selected_place.id,
                'osm_id': o.selected_place.osm_id,
                'name': o.selected_place.name,
                'latlng': o.selected_place.geom.coords[::-1],
            },
            'title': o.title,
            'pic_url': o.pic_url(),
            'markers': [{
                'id': s.id,
                'osm_id': s.place.osm_id,
                'name': s.place.name,
                'latlng': s.place.geom.coords[::-1],
                'score': s.score,
                'accepted': s.status == Suggestion.Status.ACCEPTED,
            } for s in o.suggestions.order_by('-score')],
            'geom_from_osm': o.geom_from_osm and o.geom_from_osm.coords[::-1],
            'exact_geom': {
                'latlng': o.exact_geom and o.exact_geom.coords[::-1],
                'radius': o.exact_geom_radius,
            },
        }

    def post(self, request, *args, **kwargs):
        o: Photo = self.get_object()
        data = json.loads(request.body)
        d = data.get('exact_geom')
        if d:
            if not isinstance(d, dict):
                return HttpResponseBadRequest("Bad exact geom")
            o.exact_geom = d['latlng'] and Point(d['latlng'][::-1])
            o.exact_geom_radius = d['radius'] and d['radius']
            o.save()
            return JsonResponse({'success': True})

        place = data.get('new_place')
        if place:
            with transaction.atomic():
                p, created = Place.objects.get_or_create(
                    osm_id=place['osm_id'],
                    defaults=dict(
                        name=place['name'],
                        geom=Point(place['latlng'][::-1]),
                        raw_data={},
                    )
                )
                o.set_place(p)
                o.status = o.Status.FOUND
                o.found_at = timezone.now()
                o.save()
                o.suggestions.update(status=Suggestion.Status.REJECTED)

            return JsonResponse({'success': True, 'place_id': p.id})

        n = data.get('suggestion')
        if not n or not isinstance(n, int):
            return HttpResponseBadRequest("Bad or missing suggestion")
        s: Suggestion = get_object_or_404(o.suggestions, id=n)
        with transaction.atomic():
            s.status = s.Status.ACCEPTED
            s.save()
            o.set_place(s.place)
            o.status = o.Status.FOUND
            o.found_at = timezone.now()
            o.save()
            o.suggestions.exclude(id=s.id).update(status=s.Status.REJECTED)

        return JsonResponse({'success': True})


class PhotoListAPIView(LoginRequiredMixin, View):
    def photo_as_dict(self, o: Photo):
        return {
            'id': o.id,
            'uid': o.uid,
            'status': o.status,
            'title': o.title,
            'place': o.selected_place.name if o.selected_place else None,
            'edit_url': o.get_absolute_url(),
        }

    def get(self, request):
        qs = Photo.objects.order_by('uid')
        return JsonResponse({'items': [self.photo_as_dict(o) for o in qs]})
