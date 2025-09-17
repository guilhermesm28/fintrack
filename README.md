# 📌 Projeto Streamlit - Estrutura MVC

Este projeto segue o **padrão MVC** (Model-View-Controller) para organizar o acesso a dados.
O objetivo é manter a aplicação **modular, fácil de manter e escalável**.

- **MVC** separa a aplicação em:
  - **Model** (dados),
  - **View** (interface)
  - **Controller** (lógica).

---

## 📂 Estrutura de Pastas

```plaintext
project/
│
├── models/ # Definições ORM (SQLAlchemy)
├── controllers/ # Regras de negócio e orquestração
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

### 2. **Controllers**
- Contêm as **regras de negócio** da aplicação.
- Se comunicam diretamente com o banco de dados usando SQLAlchemy.
- Orquestram chamadas entre **models** e **views**.

---

### 3. **Views**
- Camada de **interface com o usuário**, feita com **Streamlit**.
- Exibe os dados processados pelos controllers.

---

### 4. **Utils**
- Funções **auxiliares e genéricas**, sem regra de negócio.
