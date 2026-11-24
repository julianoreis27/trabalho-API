from django.db import models


class Livro(models.Model):
    """Tabela `livros` do banco de dados (SQLite)."""

    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    ano = models.PositiveIntegerField()
    genero = models.CharField(max_length=50, blank=True, default="")
    disponivel = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "livros"  # nome da tabela no banco
        ordering = ["id"]

    def __str__(self):
        return f"{self.titulo} ({self.autor})"
