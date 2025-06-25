# 📚 Documentação da API

Este projeto foi desenvolvido por **Brenda Mendes** 👩‍💻 e consiste no back-end que é consumido pelo chatbot 🤖 criado com o Microsoft Bot Framework.

## 📝 Descrição

Esta API foi desenvolvida em Python 🐍 utilizando FastAPI ⚡ e SQLAlchemy, conectando-se a um banco de dados MySQL 🛢️. Ela gerencia matrículas de alunos, permitindo criar, listar e buscar matrículas por ID.

## 🚀 Endpoints Disponíveis

### 1️⃣ Criar Matrícula
- **Endpoint:** `POST /api/matriculas`
- **Descrição:** Cria uma nova matrícula no sistema.
- **Body (JSON):**
  ```json
  {
    "nome": "Nome do Aluno",
    "email": "email@exemplo.com",
    "curso": "Nome do Curso"
  }
  ```
- **Resposta (JSON):**
  ```json
  {
    "matricula": 1,
    "nome": "Nome do Aluno",
    "email": "email@exemplo.com",
    "curso": "Nome do Curso"
  }
  ```

### 2️⃣ Listar Todas as Matrículas
- **Endpoint:** `GET /api/matriculas`
- **Descrição:** Retorna uma lista com todas as matrículas cadastradas.
- **Resposta (JSON):**
  ```json
  [
    {
      "matricula": 1,
      "nome": "Nome do Aluno",
      "email": "email@exemplo.com",
      "curso": "Nome do Curso"
    },
    ...
  ]
  ```

### 3️⃣ Buscar Matrícula por ID
- **Endpoint:** `GET /api/matriculas/{matricula_id}`
- **Descrição:** Retorna os dados de uma matrícula específica pelo ID.
- **Resposta (JSON):**
  ```json
  {
    "matricula": 1,
    "nome": "Nome do Aluno",
    "email": "email@exemplo.com",
    "curso": "Nome do Curso"
  }
  ```
- **Erro 404:**
  ```json
  { "detail": "Matrícula não encontrada" }
  ```
