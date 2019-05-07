import json

from django.db import transaction
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView

from core.models import Photo, Suggestion


class PhotoListView(ListView):
    model = Photo
    paginate_by = 25
    ordering = "?"


class PhotoDetailView(DetailView):
    model = Photo

    def app_data(self):
        o: Photo = self.get_object()
        return {
            'id': o.id,
            'title': o.title,
            'pic_url': o.pic_url(),
            'markers': [{
                'id': s.id,
                'name': s.place.name,
                'latlng': s.place.geom.coords[::-1],
                'score': s.score,
                'accepted': s.status == Suggestion.Status.ACCEPTED,
            } for s in o.suggestions.all()],
        }

    def post(self, request, *args, **kwargs):
        o: Photo = self.get_object()
        data = json.loads(request.body)
        n = data.get('suggestion')
        if not n or not isinstance(n, int):
            return HttpResponseBadRequest(f"Bad or missing suggestion")
        s: Suggestion = get_object_or_404(o.suggestions, id=n)
        with transaction.atomic():
            s.status = s.Status.ACCEPTED
            s.save()
            o.selected_place = s.place
            o.status = o.Status.FOUND
            o.found_at = timezone.now()
            o.save()

        return JsonResponse({'success': True})


class PhotoListAPIView(View):
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
