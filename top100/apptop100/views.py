from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Cancion, Estilo, Artista, Album

def home(request):
    estilos = Estilo.objects.order_by('nombre')
    destacados = []
    for estilo in estilos:
        top = Cancion.objects.filter(estilo=estilo).order_by('-reproducciones').first()
        destacados.append((estilo, top))
    context = {"destacados": destacados}
    return render(request, "home.html", context)

def index_canciones(request):
    canciones = get_list_or_404(Cancion.objects.order_by('-reproducciones'))
    context = {"songs": canciones}
    return render(request, "songs/list.html", context)

def show_cancion(request, pk):
    cancion = get_object_or_404(Cancion, pk=pk)
    context = {"song": cancion}
    return render(request, "songs/detail.html", context)

def index_estilos(request):
    estilos = get_list_or_404(Estilo.objects.order_by('nombre'))
    context = {"genres": estilos}
    return render(request, "genres/list.html", context)

def show_estilo(request, pk):
    estilo = get_object_or_404(Estilo, pk=pk)
    canciones = estilo.canciones.order_by('-reproducciones')
    context = {"genre": estilo, "songs": canciones}
    return render(request, "genres/detail.html", context)

def index_artistas(request):
    artistas = get_list_or_404(Artista.objects.order_by('nombre'))
    context = {"artists": artistas}
    return render(request, "artists/list.html", context)

def show_artista(request, pk):
    artista = get_object_or_404(Artista, pk=pk)
    canciones = artista.canciones.all()
    context = {"artist": artista, "songs": canciones}
    return render(request, "artists/detail.html", context)

def index_albumes(request):
    albumes = Album.objects.order_by('titulo')
    context = {"albumes": albumes}
    return render(request, "albums/list.html", context)

def show_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    context = {"album": album}
    return render(request, "albums/detail.html", context)
