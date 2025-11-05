from django.urls import path, include
from django.views.generic import TemplateView

songs_patterns = ([
    path("", TemplateView.as_view(template_name="songs/list.html"), name="list"),
    path("<int:pk>/", TemplateView.as_view(template_name="songs/detail.html"), name="detail"),
], "songs")

genres_patterns = ([
    path("", TemplateView.as_view(template_name="genres/list.html"), name="list"),
    path("<slug:slug>/", TemplateView.as_view(template_name="genres/detail.html"), name="detail"),
], "genres")

artists_patterns = ([
    path("", TemplateView.as_view(template_name="artists/list.html"), name="list"),
    path("<slug:slug>/", TemplateView.as_view(template_name="artists/detail.html"), name="detail"),
], "artists")

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("songs/", include(songs_patterns)),
    path("genres/", include(genres_patterns)),
    path("artists/", include(artists_patterns)),
]
