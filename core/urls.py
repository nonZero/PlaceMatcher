from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path('', views.PhotoListView.as_view(), name='list'),
    path('<int:pk>/', views.PhotoDetailView.as_view(), name='detail'),
]
