from django.contrib import admin

from .models import Album, Artista, Cancion, Estilo


class CancionInline(admin.TabularInline):
	model = Cancion
	extra = 1
	fields = ("nombre", "estilo", "duracion", "reproducciones", "fecha_lanzamiento")
	show_change_link = True


class ArtistaCancionInline(admin.TabularInline):
	model = Cancion.artistas.through
	fk_name = "artista"
	extra = 1
	verbose_name = "Canción"
	verbose_name_plural = "Canciones"
	raw_id_fields = ("cancion",)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
	list_display = ("titulo", "fecha_lanzamiento", "total_canciones", "canciones_count")
	list_filter = ("fecha_lanzamiento",)
	search_fields = ("titulo", "artistas__nombre")
	filter_horizontal = ("artistas",)
	inlines = (CancionInline,)

	@admin.display(description="Canciones")
	def canciones_count(self, obj):
		return obj.canciones.count()


class CancionArtistaFilter(admin.SimpleListFilter):
	title = "Intérprete"
	parameter_name = "artista"

	def lookups(self, request, model_admin):
		artistas = Artista.objects.order_by("nombre").values_list("id", "nombre")
		return artistas

	def queryset(self, request, queryset):
		if self.value():
			return queryset.filter(artistas__id=self.value())
		return queryset


@admin.register(Cancion)
class CancionAdmin(admin.ModelAdmin):
	list_display = (
		"nombre",
		"estilo",
		"album",
		"reproducciones",
		"duracion",
		"fecha_lanzamiento",
	)
	list_filter = ("estilo", "fecha_lanzamiento", CancionArtistaFilter)
	search_fields = ("nombre", "artistas__nombre", "album__titulo")
	raw_id_fields = ("album",)
	filter_horizontal = ("artistas",)
	date_hierarchy = "fecha_lanzamiento"
	ordering = ("-reproducciones", "nombre")
	list_per_page = 25
	fieldsets = (
		(
			"Ficha",
			{"fields": ("nombre", "estilo", "album", "artistas")},
		),
		(
			"Datos de rendimiento",
			{"fields": ("reproducciones", "duracion", "fecha_lanzamiento")},
		),
	)


@admin.register(Artista)
class ArtistaAdmin(admin.ModelAdmin):
	list_display = ("nombre", "nacionalidad", "popularidad", "followers")
	list_filter = ("nacionalidad",)
	search_fields = ("nombre", "nacionalidad")
	inlines = (ArtistaCancionInline,)
	readonly_fields = ("popularidad", "followers")
	fieldsets = (
		("Identidad", {"fields": ("nombre", "nacionalidad", "imagen", "fecha_nacimiento")}),
		("Métricas", {"fields": ("popularidad", "followers"), "classes": ("collapse",)}),
	)


@admin.register(Estilo)
class EstiloAdmin(admin.ModelAdmin):
	list_display = ("nombre", "descripcion")
	search_fields = ("nombre", "descripcion")
	ordering = ("nombre",)


admin.site.site_header = "Top 100 · Administración"
admin.site.site_title = "Panel Top 100"
admin.site.index_title = "Gestión de música"
