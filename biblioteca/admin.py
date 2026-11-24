from django.contrib import admin

from .models import Livro


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ["id", "titulo", "autor", "ano", "genero", "disponivel", "criado_em"]
    list_filter = ["disponivel", "genero"]
    search_fields = ["titulo", "autor"]
