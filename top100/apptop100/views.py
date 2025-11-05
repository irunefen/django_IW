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
    canciones = Cancion.objects.order_by('-reproducciones')
    context = {"songs": canciones}
    return render(request, "songs/list.html", context)

def show_cancion(request, pk):
    cancion = get_object_or_404(Cancion, pk=pk)
    context = {"song": cancion}
    return render(request, "songs/detail.html", context)

def index_estilos(request):
    estilos = Estilo.objects.order_by('nombre')
    context = {"genres": estilos}
    return render(request, "genres/list.html", context)

def show_estilo(request, slug):
    from django.utils.text import slugify
    estilos = Estilo.objects.all()
    estilo = None
    for e in estilos:
        if slugify(e.nombre) == slug:
            estilo = e
            break
    if not estilo:
        estilo = get_object_or_404(Estilo, nombre__iexact=slug.replace('-', ' '))
    canciones = Cancion.objects.filter(estilo=estilo).order_by('-reproducciones')
    context = {"genre": estilo, "songs": canciones}
    return render(request, "genres/detail.html", context)

def index_artistas(request):
    artistas = Artista.objects.order_by('nombre')
    context = {"artists": artistas}
    return render(request, "artists/list.html", context)

def show_artista(request, slug):
    from django.utils.text import slugify
    artistas = Artista.objects.all()
    artista = None
    for a in artistas:
        if slugify(a.nombre) == slug:
            artista = a
            break
    if not artista:
        artista = get_object_or_404(Artista, nombre__iexact=slug.replace('-', ' '))
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
