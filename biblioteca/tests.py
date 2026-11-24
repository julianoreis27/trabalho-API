"""Testes automatizados dos 10 endpoints.

Executar:  python manage.py test
(O banco de testes já vem com os 5 livros da migração 0002_dados_iniciais.)
"""

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Livro

NOVO_LIVRO = {"titulo": "O Alquimista", "autor": "Paulo Coelho", "ano": 1988, "genero": "Romance"}


class CrudTests(APITestCase):
    # 1) POST /api/livros/
    def test_criar_livro(self):
        resposta = self.client.post("/api/livros/", NOVO_LIVRO, format="json")
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resposta.data["titulo"], "O Alquimista")
        self.assertTrue(resposta.data["disponivel"])
        self.assertTrue(Livro.objects.filter(titulo="O Alquimista").exists())

    def test_criar_livro_invalido(self):
        resposta = self.client.post("/api/livros/", {"titulo": ""}, format="json")
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("autor", resposta.data)

    def test_criar_livro_com_ano_futuro(self):
        dados = {**NOVO_LIVRO, "ano": 3000}
        resposta = self.client.post("/api/livros/", dados, format="json")
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("ano", resposta.data)

    # 2) GET /api/livros/
    def test_listar_livros(self):
        resposta = self.client.get("/api/livros/")
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), Livro.objects.count())

    # 3) PUT /api/livros/<id>/
    def test_atualizar_livro(self):
        livro = Livro.objects.create(**NOVO_LIVRO)
        dados = {**NOVO_LIVRO, "titulo": "O Alquimista (edição especial)"}
        resposta = self.client.put(f"/api/livros/{livro.id}/", dados, format="json")
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        livro.refresh_from_db()
        self.assertEqual(livro.titulo, "O Alquimista (edição especial)")

    def test_atualizar_livro_inexistente(self):
        resposta = self.client.put("/api/livros/9999/", NOVO_LIVRO, format="json")
        self.assertEqual(resposta.status_code, status.HTTP_404_NOT_FOUND)

    # 4) DELETE /api/livros/<id>/
    def test_excluir_livro(self):
        livro = Livro.objects.create(**NOVO_LIVRO)
        resposta = self.client.delete(f"/api/livros/{livro.id}/")
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertFalse(Livro.objects.filter(id=livro.id).exists())

    def test_excluir_livro_inexistente(self):
        resposta = self.client.delete("/api/livros/9999/")
        self.assertEqual(resposta.status_code, status.HTTP_404_NOT_FOUND)


class BuscaPorIdTests(APITestCase):
    # 5) GET /api/livros/<id>/
    def test_buscar_por_id(self):
        livro = Livro.objects.create(**NOVO_LIVRO)
        resposta = self.client.get(f"/api/livros/{livro.id}/")
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data["id"], livro.id)
        self.assertEqual(resposta.data["autor"], "Paulo Coelho")

    def test_buscar_por_id_inexistente(self):
        resposta = self.client.get("/api/livros/9999/")
        self.assertEqual(resposta.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(resposta.data["detail"], "Livro 9999 não encontrado.")


class ConsultasTests(APITestCase):
    # 6) GET /api/livros/buscar/?termo=
    def test_buscar_por_autor_sem_diferenciar_maiusculas(self):
        resposta = self.client.get("/api/livros/buscar/", {"termo": "machado"})
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual([livro["titulo"] for livro in resposta.data], ["Dom Casmurro"])

    def test_buscar_por_titulo(self):
        resposta = self.client.get("/api/livros/buscar/", {"termo": "Hobbit"})
        self.assertEqual(len(resposta.data), 1)

    def test_buscar_sem_termo(self):
        resposta = self.client.get("/api/livros/buscar/")
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)

    # 7) GET /api/livros/disponiveis/
    def test_listar_disponiveis(self):
        emprestado = Livro.objects.create(**NOVO_LIVRO, disponivel=False)
        resposta = self.client.get("/api/livros/disponiveis/")
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        ids = [livro["id"] for livro in resposta.data]
        self.assertNotIn(emprestado.id, ids)
        self.assertTrue(all(livro["disponivel"] for livro in resposta.data))

    # 8) GET /api/estatisticas/
    def test_estatisticas(self):
        Livro.objects.create(**NOVO_LIVRO, disponivel=False)
        resposta = self.client.get("/api/estatisticas/")
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data["total"], 6)
        self.assertEqual(resposta.data["disponiveis"], 5)
        self.assertEqual(resposta.data["emprestados"], 1)
        self.assertEqual(resposta.data["por_genero"]["Romance"], 3)


class EmprestimoTests(APITestCase):
    def setUp(self):
        self.livro = Livro.objects.create(**NOVO_LIVRO)

    # 9) PATCH /api/livros/<id>/emprestar/
    def test_emprestar(self):
        resposta = self.client.patch(f"/api/livros/{self.livro.id}/emprestar/")
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertFalse(resposta.data["disponivel"])

    def test_emprestar_livro_ja_emprestado(self):
        self.client.patch(f"/api/livros/{self.livro.id}/emprestar/")
        resposta = self.client.patch(f"/api/livros/{self.livro.id}/emprestar/")
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)

    # 10) PATCH /api/livros/<id>/devolver/
    def test_devolver(self):
        self.client.patch(f"/api/livros/{self.livro.id}/emprestar/")
        resposta = self.client.patch(f"/api/livros/{self.livro.id}/devolver/")
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertTrue(resposta.data["disponivel"])

    def test_devolver_livro_nao_emprestado(self):
        resposta = self.client.patch(f"/api/livros/{self.livro.id}/devolver/")
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)

    def test_emprestar_livro_inexistente(self):
        resposta = self.client.patch("/api/livros/9999/emprestar/")
        self.assertEqual(resposta.status_code, status.HTTP_404_NOT_FOUND)
