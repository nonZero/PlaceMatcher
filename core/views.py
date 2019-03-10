from django.views.generic import ListView, DetailView

from core.models import Photo


class PhotoListView(ListView):
    model = Photo
    paginate_by = 25
    ordering = "?"


class PhotoDetailView(DetailView):
    model = Photo
