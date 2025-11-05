from django.db import models

class Estilo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
        
class Artista(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    followers = models.IntegerField()
    imagen = models.URLField(blank=True)
    popularidad = models.IntegerField()
    nacionalidad = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombre
    
class Album(models.Model):
    titulo = models.CharField(max_length=200)
    artistas = models.ManyToManyField(Artista, related_name='albumes')
    fecha_lanzamiento = models.DateField(blank=True, null=True)
    total_canciones = models.IntegerField()
    imagen = models.URLField(blank=True)

    def __str__(self):
        return self.titulo

class Cancion(models.Model):
    nombre = models.CharField(max_length=200)
    artistas = models.ManyToManyField(Artista, related_name='canciones')
    estilo = models.ForeignKey(Estilo, on_delete=models.CASCADE, related_name='canciones')
    reproducciones = models.IntegerField()
    duracion = models.IntegerField(help_text="Duración en segundos")
    fecha_lanzamiento = models.DateField(blank=True, null=True)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, blank=True, null=True, related_name='canciones')

    def __str__(self):
        artistas_nombres = ", ".join([artista.nombre for artista in self.artistas.all()])
        return f"{self.nombre} - {artistas_nombres}" if artistas_nombres else self.nombre