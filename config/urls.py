from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Painel administrativo do Django (opcional, para visualizar a tabela)
    path("admin/", admin.site.urls),
    # Endpoints da API
    path("api/", include("biblioteca.urls")),
]
