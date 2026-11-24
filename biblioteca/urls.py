from django.urls import path

from . import views

# Todas as rotas abaixo ficam sob o prefixo /api/ (ver config/urls.py).
urlpatterns = [
    # 1) POST  e  2) GET
    path("livros/", views.LivroListaView.as_view(), name="livros"),
    # 6) GET
    path("livros/buscar/", views.buscar_livros, name="livros-buscar"),
    # 7) GET
    path("livros/disponiveis/", views.livros_disponiveis, name="livros-disponiveis"),
    # 5) GET  ,  3) PUT  e  4) DELETE
    path("livros/<int:pk>/", views.LivroDetalheView.as_view(), name="livro-detalhe"),
    # 9) PATCH
    path("livros/<int:pk>/emprestar/", views.emprestar_livro, name="livro-emprestar"),
    # 10) PATCH
    path("livros/<int:pk>/devolver/", views.devolver_livro, name="livro-devolver"),
    # 8) GET
    path("estatisticas/", views.estatisticas, name="estatisticas"),
]
