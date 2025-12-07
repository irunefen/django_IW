from django.urls import path, include
from . import views

songs_patterns = ([
    path('', views.index_canciones, name='list'),
    path('<int:pk>/', views.show_cancion, name='detail'),
], 'songs')

genres_patterns = ([
    path('', views.index_estilos, name='list'),
    path('<int:pk>/', views.show_estilo, name='detail'),
], 'genres')

artists_patterns = ([
    path('', views.index_artistas, name='list'),
    path('<int:pk>/', views.show_artista, name='detail'),
], 'artists')


urlpatterns = [
    path('', views.home, name='home'),
    path('songs/', include(songs_patterns)),
    path('genres/', include(genres_patterns)),
    path('artists/', include(artists_patterns)),
    path('albumes/', views.index_albumes, name='albumes_list'),
    path('albumes/<int:album_id>/', views.show_album, name='album_detail'),
]
