# API Biblioteca — Django REST Framework

Trabalho da disciplina **Desenvolvimento de Serviços e API**.

API REST simples para gerenciar os livros de uma biblioteca: cadastrar, listar,
atualizar, excluir, buscar, emprestar e devolver livros.

| Requisito do trabalho              | Como foi atendido                                         |
|------------------------------------|-----------------------------------------------------------|
| 10 endpoints                       | 10 endpoints (tabela abaixo)                              |
| CRUD (4 endpoints)                 | `POST`, `GET`, `PUT` e `DELETE` em `/api/livros/`         |
| 1 endpoint de busca por ID         | `GET /api/livros/<id>/`                                   |
| No mínimo 1 tabela no banco        | Tabela `livros` no SQLite                                 |

## Tecnologias

- **Python 3.10+**
- **Django 5.2** — framework web
- **Django REST Framework** — criação da API REST
- **SQLite** — banco de dados (já vem com o Python, não precisa instalar nada)

## Endpoints

URL base: `http://127.0.0.1:8000/api`

| #  | Método   | Rota                                | Descrição                                   | Grupo        |
|----|----------|-------------------------------------|---------------------------------------------|--------------|
| 1  | `POST`   | `/api/livros/`                      | Cadastra um novo livro                      | CRUD         |
| 2  | `GET`    | `/api/livros/`                      | Lista todos os livros                       | CRUD         |
| 3  | `PUT`    | `/api/livros/<id>/`                 | Atualiza os dados de um livro               | CRUD         |
| 4  | `DELETE` | `/api/livros/<id>/`                 | Exclui um livro                             | CRUD         |
| 5  | `GET`    | `/api/livros/<id>/`                 | Busca um livro pelo **ID**                  | Busca por ID |
| 6  | `GET`    | `/api/livros/buscar/?termo=machado` | Busca por parte do título ou do autor       | Consultas    |
| 7  | `GET`    | `/api/livros/disponiveis/`          | Lista só os livros disponíveis              | Consultas    |
| 8  | `GET`    | `/api/estatisticas/`                | Total, disponíveis, emprestados e por gênero | Consultas    |
| 9  | `PATCH`  | `/api/livros/<id>/emprestar/`       | Empresta um livro                           | Empréstimos  |
| 10 | `PATCH`  | `/api/livros/<id>/devolver/`        | Devolve um livro                            | Empréstimos  |

### Códigos de resposta usados

| Código | Quando acontece                                                          |
|--------|--------------------------------------------------------------------------|
| `200`  | Requisição feita com sucesso                                             |
| `201`  | Livro cadastrado (POST)                                                  |
| `400`  | Dados inválidos, busca sem `termo`, emprestar livro já emprestado, etc.  |
| `404`  | Livro com o ID informado não existe                                      |
| `405`  | Método HTTP não permitido na rota                                        |

### Exemplo de corpo (JSON) para `POST` e `PUT`

```json
{
  "titulo": "O Alquimista",
  "autor": "Paulo Coelho",
  "ano": 1988,
  "genero": "Romance"
}
```

Validações: `titulo`, `autor` e `ano` são obrigatórios; `ano` não pode ser
negativo nem maior que o ano atual; `genero` é opcional. Os campos `id`,
`disponivel` e `criado_em` são preenchidos pelo sistema.

## Banco de dados

Tabela **`livros`** (definida em `biblioteca/models.py`):

| Coluna       | Tipo         | Observação                                  |
|--------------|--------------|---------------------------------------------|
| `id`         | inteiro      | Chave primária, autoincremento              |
| `titulo`     | texto (200)  | Obrigatório                                 |
| `autor`      | texto (100)  | Obrigatório                                 |
| `ano`        | inteiro      | Obrigatório                                 |
| `genero`     | texto (50)   | Opcional                                    |
| `disponivel` | booleano     | `true` ao cadastrar; muda ao emprestar/devolver |
| `criado_em`  | data/hora    | Preenchido automaticamente                  |

Ao rodar `python manage.py migrate`, a tabela é criada e **5 livros de exemplo**
são inseridos automaticamente (migração `0002_dados_iniciais.py`).

## Como executar

```bash
# 1. Clonar o repositório
git clone https://github.com/julianoreis27/trabalho-API.git
cd trabalho-API

# 2. Criar e ativar o ambiente virtual
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux / macOS

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Criar o banco de dados e a tabela (já insere 5 livros de exemplo)
python manage.py migrate

# 5. Iniciar o servidor
python manage.py runserver
```

Pronto! Acesse **http://127.0.0.1:8000/api/livros/** no navegador.

### Variáveis de ambiente (opcional)

Para apresentar **não é preciso definir nada**: sem variáveis, o projeto roda em
modo de desenvolvimento. Elas existem para não deixar configurações sensíveis
fixas no código (boa prática para quando o projeto for publicado):

| Variável               | Padrão                     | Para que serve                          |
|------------------------|----------------------------|-----------------------------------------|
| `DJANGO_SECRET_KEY`    | chave de desenvolvimento   | Chave secreta do Django                 |
| `DJANGO_DEBUG`         | `True`                     | `False` desliga o modo de depuração     |
| `DJANGO_ALLOWED_HOSTS` | `*`                        | Domínios aceitos, separados por vírgula |

## Como testar

### 1. Pelo navegador (interface do Django REST Framework)

O DRF gera páginas onde dá para ver o JSON e enviar requisições pelos botões
(`GET`, `POST`, `PUT`, `DELETE`, `PATCH`) — ótimo para a apresentação:

- http://127.0.0.1:8000/api/livros/ — lista e formulário de cadastro (POST)
- http://127.0.0.1:8000/api/livros/1/ — busca por ID, edição (PUT) e exclusão (DELETE)
- http://127.0.0.1:8000/api/livros/buscar/?termo=machado
- http://127.0.0.1:8000/api/livros/disponiveis/
- http://127.0.0.1:8000/api/estatisticas/
- http://127.0.0.1:8000/api/livros/1/emprestar/ — clique no botão **PATCH**
- http://127.0.0.1:8000/api/livros/1/devolver/ — clique no botão **PATCH**

> Em `emprestar/` e `devolver/` o navegador mostra "405 Method Not Allowed"
> ao abrir a página, porque ela só aceita `PATCH`. É só clicar no botão PATCH.

### 2. Pelo Postman / Insomnia

Importe o arquivo **`postman_collection.json`**. Ele já tem as 10 requisições
organizadas em pastas. A variável `id` vem como `6` (o ID do primeiro livro
cadastrado pelo POST); altere-a se necessário.

### 3. Pelo terminal (curl — Linux, macOS ou Git Bash)

```bash
curl -X POST http://127.0.0.1:8000/api/livros/ -H "Content-Type: application/json" -d '{"titulo": "O Alquimista", "autor": "Paulo Coelho", "ano": 1988, "genero": "Romance"}'
curl http://127.0.0.1:8000/api/livros/
curl http://127.0.0.1:8000/api/livros/6/
curl -X PUT http://127.0.0.1:8000/api/livros/6/ -H "Content-Type: application/json" -d '{"titulo": "O Alquimista (edição especial)", "autor": "Paulo Coelho", "ano": 1988, "genero": "Romance"}'
curl "http://127.0.0.1:8000/api/livros/buscar/?termo=machado"
curl -X PATCH http://127.0.0.1:8000/api/livros/6/emprestar/
curl http://127.0.0.1:8000/api/livros/disponiveis/
curl http://127.0.0.1:8000/api/estatisticas/
curl -X PATCH http://127.0.0.1:8000/api/livros/6/devolver/
curl -X DELETE http://127.0.0.1:8000/api/livros/6/
```

### 4. Testes automatizados

```bash
python manage.py test
```

São 20 testes cobrindo os 10 endpoints, incluindo os casos de erro (404, 400).

### (Opcional) Painel administrativo do Django

Para ver a tabela `livros` em uma tela pronta do Django:

```bash
python manage.py createsuperuser
```

Depois acesse http://127.0.0.1:8000/admin/ (não faz parte dos 10 endpoints da API).

## Roteiro sugerido para a apresentação

1. Mostrar a tabela `livros` em `biblioteca/models.py` (e o admin, se quiser).
2. **GET** `/api/livros/` → lista os 5 livros de exemplo.
3. **POST** `/api/livros/` → cadastrar "O Alquimista" (resposta `201`, recebe o id 6).
4. **GET** `/api/livros/6/` → busca por ID. Mostrar também `/api/livros/99/` → `404`.
5. **PUT** `/api/livros/6/` → alterar o título.
6. **GET** `/api/livros/buscar/?termo=machado` → busca por autor.
7. **PATCH** `/api/livros/6/emprestar/` → livro fica `"disponivel": false`.
   Repetir o PATCH → `400` "Este livro já está emprestado" (regra de negócio).
8. **GET** `/api/livros/disponiveis/` e **GET** `/api/estatisticas/` → o livro 6 aparece como emprestado.
9. **PATCH** `/api/livros/6/devolver/` → livro volta a ficar disponível.
10. **DELETE** `/api/livros/6/` → exclui o livro.
11. Extra: **POST** com dados inválidos (ex.: sem autor) → `400` com as mensagens de validação.

## Estrutura do projeto

```
trabalho-API/
├── manage.py                  # utilitário de linha de comando do Django
├── requirements.txt           # dependências
├── postman_collection.json    # coleção com as 10 requisições
├── config/                    # configurações do projeto Django
│   ├── settings.py
│   └── urls.py                # rota /api/ -> biblioteca.urls
└── biblioteca/                # app da API
    ├── models.py              # tabela "livros"
    ├── serializers.py         # conversão Livro <-> JSON + validações
    ├── views.py               # os 10 endpoints
    ├── urls.py                # rotas da API
    ├── admin.py               # registro no painel admin
    ├── tests.py               # testes automatizados
    └── migrations/            # criação da tabela + dados de exemplo
```

## Fluxo de uma requisição

```
Cliente (navegador/Postman)
   │  HTTP + JSON
   ▼
config/urls.py  ──►  biblioteca/urls.py  ──►  views.py
                                               │
                                 serializers.py (valida / converte JSON)
                                               │
                                     models.py (ORM do Django)
                                               │
                                     SQLite (tabela "livros")
```
