# 📌 Projeto Streamlit - Estrutura MVC + Repository Pattern

Este projeto segue uma **variação do padrão MVC** (Model-View-Controller), incorporando o **Repository Pattern** para organizar o acesso a dados.
O objetivo é manter a aplicação **modular, fácil de manter e escalável**.

- **MVC** separa a aplicação em:
  - **Model** (dados),
  - **View** (interface)
  - **Controller** (lógica).

- **Repository Pattern** adiciona uma camada a mais para **isolar o acesso a dados**.
  Isso evita acoplamento direto entre **Controllers** e **Banco de Dados**.

---

## 📂 Estrutura de Pastas

```plaintext
project/
│
├── models/ # Definições ORM (SQLAlchemy)
├── repositories/ # Acesso a dados (CRUD) usando Repositories Pattern
├── controllers/ # Regras de negócio / orquestração
├── views/ # Telas do Streamlit (UI)
└── utils/ # Funções auxiliares
```

---

## 🔹 Explicação dos Módulos

### 1. **Models**
- Contém as **entidades do domínio**, mapeadas via SQLAlchemy ORM.
- Cada classe representa uma tabela do banco de dados.
- Mantém apenas **atributos e relacionamentos** (sem regras de negócio complexas).

---

### 2. **Repositories** (Repository Pattern)
- Responsáveis pelo **acesso aos dados** (CRUD).
- Se comunicam diretamente com o banco de dados usando SQLAlchemy.
- Abstraem a lógica de persistência, evitando SQL espalhado pelo código.

---

### 3. **Controllers**
- Contêm as **regras de negócio** da aplicação.
- Orquestram chamadas entre **repositories** e **views**.

---

### 4. **Views**
- Camada de **interface com o usuário**, feita com **Streamlit**.
- Exibe os dados processados pelos controllers.

---

### 5. **Utils**
- Funções **auxiliares e genéricas**, sem regra de negócio.
