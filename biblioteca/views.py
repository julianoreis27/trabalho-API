"""Endpoints da API Biblioteca.

Resumo dos 10 endpoints:

  CRUD
    1) POST   /api/livros/                   -> cadastrar livro
    2) GET    /api/livros/                   -> listar livros
    3) PUT    /api/livros/<id>/              -> atualizar livro
    4) DELETE /api/livros/<id>/              -> excluir livro
  Busca por ID
    5) GET    /api/livros/<id>/              -> buscar livro pelo ID
  Consultas
    6) GET    /api/livros/buscar/?termo=...  -> buscar por título ou autor
    7) GET    /api/livros/disponiveis/       -> listar livros disponíveis
    8) GET    /api/estatisticas/             -> estatísticas do acervo
  Empréstimos
    9) PATCH  /api/livros/<id>/emprestar/    -> emprestar livro
   10) PATCH  /api/livros/<id>/devolver/     -> devolver livro
"""

from django.db.models import Count, Q
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import Livro
from .serializers import LivroSerializer


def buscar_livro(pk):
    """Busca um livro pelo ID ou devolve erro 404 (Not Found)."""
    try:
        return Livro.objects.get(pk=pk)
    except Livro.DoesNotExist:
        raise NotFound(f"Livro {pk} não encontrado.")


# ---------------------------------------------------------------------------
# /api/livros/
# (queryset e serializer_class são usados pela interface navegável do DRF
#  para montar o formulário HTML de cadastro/edição)
# ---------------------------------------------------------------------------

class LivroListaView(generics.GenericAPIView):
    """GET lista todos os livros (endpoint 2) | POST cadastra um livro (endpoint 1)."""

    queryset = Livro.objects.all()
    serializer_class = LivroSerializer

    # 2) READ - lista todos os livros
    def get(self, request):
        livros = Livro.objects.all()
        serializer = LivroSerializer(livros, many=True)
        return Response(serializer.data)

    # 1) CREATE - cadastra um novo livro
    def post(self, request):
        serializer = LivroSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # devolve 400 se os dados forem inválidos
        serializer.save()  # INSERT no banco
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ---------------------------------------------------------------------------
# /api/livros/<id>/
# ---------------------------------------------------------------------------

class LivroDetalheView(generics.GenericAPIView):
    """GET busca pelo ID (endpoint 5) | PUT atualiza (endpoint 3) | DELETE exclui (endpoint 4)."""

    queryset = Livro.objects.all()
    serializer_class = LivroSerializer

    # 5) Busca um livro pelo ID
    def get(self, request, pk):
        livro = buscar_livro(pk)
        return Response(LivroSerializer(livro).data)

    # 3) UPDATE - atualiza os dados de um livro
    def put(self, request, pk):
        livro = buscar_livro(pk)
        serializer = LivroSerializer(livro, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # UPDATE no banco
        return Response(serializer.data)

    # 4) DELETE - exclui um livro
    def delete(self, request, pk):
        livro = buscar_livro(pk)
        titulo = livro.titulo
        livro.delete()  # DELETE no banco
        return Response({"mensagem": f"Livro '{titulo}' (id {pk}) excluído com sucesso."})


# ---------------------------------------------------------------------------
# Consultas
# ---------------------------------------------------------------------------

# 6) Busca livros por parte do título ou do autor
@api_view(["GET"])
def buscar_livros(request):
    """Busca livros por parte do título ou do autor. Ex.: ?termo=machado"""
    termo = request.query_params.get("termo", "").strip()
    if not termo:
        return Response(
            {"detail": "Informe o parâmetro 'termo'. Ex.: /api/livros/buscar/?termo=machado"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    livros = Livro.objects.filter(Q(titulo__icontains=termo) | Q(autor__icontains=termo))
    return Response(LivroSerializer(livros, many=True).data)


# 7) Lista apenas os livros disponíveis para empréstimo
@api_view(["GET"])
def livros_disponiveis(request):
    """Lista apenas os livros disponíveis para empréstimo."""
    livros = Livro.objects.filter(disponivel=True)
    return Response(LivroSerializer(livros, many=True).data)


# 8) Estatísticas do acervo
@api_view(["GET"])
def estatisticas(request):
    """Total de livros, disponíveis, emprestados e quantidade por gênero."""
    total = Livro.objects.count()
    disponiveis = Livro.objects.filter(disponivel=True).count()
    generos = (
        Livro.objects.values("genero")
        .annotate(quantidade=Count("id"))
        .order_by("-quantidade", "genero")
    )
    return Response(
        {
            "total": total,
            "disponiveis": disponiveis,
            "emprestados": total - disponiveis,
            "por_genero": {g["genero"] or "Sem gênero": g["quantidade"] for g in generos},
        }
    )


# ---------------------------------------------------------------------------
# Empréstimos (regras de negócio)
# ---------------------------------------------------------------------------

# 9) Empresta um livro (só se ele estiver disponível)
@api_view(["PATCH"])
def emprestar_livro(request, pk):
    """Marca o livro como emprestado (clique em PATCH, sem corpo)."""
    livro = buscar_livro(pk)
    if not livro.disponivel:
        return Response(
            {"detail": "Este livro já está emprestado."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    livro.disponivel = False
    livro.save()
    return Response(LivroSerializer(livro).data)


# 10) Devolve um livro (só se ele estiver emprestado)
@api_view(["PATCH"])
def devolver_livro(request, pk):
    """Marca o livro como devolvido/disponível (clique em PATCH, sem corpo)."""
    livro = buscar_livro(pk)
    if livro.disponivel:
        return Response(
            {"detail": "Este livro não está emprestado."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    livro.disponivel = True
    livro.save()
    return Response(LivroSerializer(livro).data)
