from django.contrib import admin
from .models import Cancion, Estilo, Artista, Album

admin.site.register(Cancion)
admin.site.register(Estilo)
admin.site.register(Artista)
admin.site.register(Album)
