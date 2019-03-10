import json

from django.http import HttpRequest
from django.views.generic import ListView, DetailView

from core.models import Photo


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
            } for s in o.suggestions.all()],
        }

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = json.loads(request.body)

