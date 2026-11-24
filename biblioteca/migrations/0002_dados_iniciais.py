"""Migração de dados: insere alguns livros de exemplo para a apresentação."""

from django.db import migrations

LIVROS_INICIAIS = [
    {"titulo": "Dom Casmurro", "autor": "Machado de Assis", "ano": 1899, "genero": "Romance"},
    {"titulo": "O Hobbit", "autor": "J. R. R. Tolkien", "ano": 1937, "genero": "Fantasia"},
    {"titulo": "1984", "autor": "George Orwell", "ano": 1949, "genero": "Ficção Científica"},
    {"titulo": "Capitães da Areia", "autor": "Jorge Amado", "ano": 1937, "genero": "Romance"},
    {"titulo": "Código Limpo", "autor": "Robert C. Martin", "ano": 2008, "genero": "Tecnologia"},
]


def inserir_livros(apps, schema_editor):
    Livro = apps.get_model("biblioteca", "Livro")
    Livro.objects.bulk_create(Livro(**dados) for dados in LIVROS_INICIAIS)


def remover_livros(apps, schema_editor):
    Livro = apps.get_model("biblioteca", "Livro")
    for dados in LIVROS_INICIAIS:
        Livro.objects.filter(titulo=dados["titulo"], autor=dados["autor"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("biblioteca", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(inserir_livros, remover_livros),
    ]
