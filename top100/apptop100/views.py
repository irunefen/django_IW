from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Cancion, Estilo, Artista, Album

from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_GET

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

@require_GET
def songs_api(request):
    q = request.GET.get("q", "").strip()

    qs = (
        Cancion.objects
        .select_related("estilo")
        .prefetch_related("artistas")
        .all()
        .order_by("-reproducciones")
    )

    if q:
        qs = qs.filter(nombre__icontains=q)

    data = []
    for song in qs[:50]:
        data.append({
            "id": song.pk,
            "name": song.nombre,
            "genre": song.estilo.nombre if song.estilo else "",
            "artists": ", ".join(a.nombre for a in song.artistas.all()),
            "detail_url": reverse("songs:detail", args=[song.pk]),
            "genre_url": reverse("genres:detail", args=[song.estilo.pk]) if song.estilo else "",
        })

    return JsonResponse({"results": data})

def global_search_api(request):
    q = request.GET.get("q", "").strip()
    if not q:
        return JsonResponse(
            {"songs": [], "artists": [], "genres": [], "albums": []}
        )

    # Limita resultados para no petar la UI
    songs_qs = Cancion.objects.filter(nombre__icontains=q)[:5]
    artists_qs = Artista.objects.filter(nombre__icontains=q)[:5]
    genres_qs = Estilo.objects.filter(nombre__icontains=q)[:5]
    albums_qs = Album.objects.filter(titulo__icontains=q)[:5]

    data = {
        "songs": [
            {
                "type": "song",
                "name": s.nombre,
                "subtitle": s.estilo.nombre if getattr(s, "estilo", None) else "",
                "url": reverse("songs:detail", args=[s.pk]),
            }
            for s in songs_qs
        ],
        "artists": [
            {
                "type": "artist",
                "name": a.nombre,
                "subtitle": "",
                "url": reverse("artists:detail", args=[a.pk]),
            }
            for a in artists_qs
        ],
        "genres": [
            {
                "type": "genre",
                "name": g.nombre,
                "subtitle": "",
                "url": reverse("genres:detail", args=[g.pk]),
            }
            for g in genres_qs
        ],
        "albums": [
            {
                "type": "album",
                "name": alb.titulo,
                "subtitle": "",
                "url": reverse("album_detail", args=[alb.pk]),
            }
            for alb in albums_qs
        ],
    }
    return JsonResponse(data)