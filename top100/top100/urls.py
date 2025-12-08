from django.contrib import admin
from django.urls import path, include
from apptop100 import views as core_views
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    # Soporte para cambiar de idioma 
    path("i18n/", include("django.conf.urls.i18n")),

    # Admin
    path("admin/", admin.site.urls),

    # API de búsqueda global
    path("search/api/", core_views.global_search_api, name="global_search_api"),
]

# URLs con soporte multiidioma 
urlpatterns += i18n_patterns(
    path("", include("apptop100.urls")),
    prefix_default_language=True,
)
