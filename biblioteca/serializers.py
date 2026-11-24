from datetime import date

from rest_framework import serializers

from .models import Livro


class LivroSerializer(serializers.ModelSerializer):
    """Converte Livro <-> JSON e valida os dados recebidos."""

    class Meta:
        model = Livro
        fields = ["id", "titulo", "autor", "ano", "genero", "disponivel", "criado_em"]
        # Campos que o cliente não pode alterar diretamente.
        # "disponivel" só muda pelos endpoints de emprestar/devolver.
        read_only_fields = ["id", "disponivel", "criado_em"]

    def validate_ano(self, valor):
        if valor > date.today().year:
            raise serializers.ValidationError("O ano não pode ser maior que o ano atual.")
        return valor
