# 📌 Projeto Streamlit - Estruturas MVC e CRUD simples

Este projeto possui dois exemplos de estrutura:
1. **MVC** (Model-View-Controller) para organizar o acesso a dados.
2. **CRUD** (Create, Read, Update, Delete) para interação com o banco de dados.

O objetivo é manter a aplicação **modular, fácil de manter e escalável**, seja utilizando uma estrutura mais robusta como o MVC ou simples como um CRUD.

- **MVC** separa a aplicação em:
  - **Model** (dados),
  - **View** (interface)
  - **Controller** (lógica).

- **CRUD** (Create, Read, Update, Delete) simplifica a interação com o banco de dados.

---

## 📂 Estrutura de Pastas

```plaintext
project/
│
├── models/ # Definições ORM (SQLAlchemy) - MVC
├── controllers/ # Regras de negócio e orquestração - MVC
├── views/ # Telas do Streamlit (UI) - MVC
├── src/ # Telas do Streamlit (UI) - CRUD
└── utils/ # Funções auxiliares - MVC e CRUD
```

---

## 🔹 Explicação dos módulos

### 1. **MODELS**
- Contém as **entidades do domínio**, mapeadas via SQLAlchemy ORM.
- Cada classe representa uma tabela do banco de dados.
- Mantém apenas **atributos e relacionamentos** (sem regras de negócio complexas).

---

### 2. **CONTROLLERS**
- Contêm as **regras de negócio** da aplicação.
- Se comunicam diretamente com o banco de dados usando SQLAlchemy.
- Orquestram chamadas entre **models** e **views**.

---

### 3. **VIEWS**
- Camada de **interface com o usuário**, feita com **Streamlit**.
- Exibe os dados processados pelos controllers.

---

### 4. **SRC**
- Camada de **interface com o usuário**, feita com **Streamlit**.
- Utiliza **CRUD** para interação com o banco de dados.

---

### 5. **UTILS**
- Funções **auxiliares e genéricas**, sem regra de negócio.
- Aqui se encontra o arquivo **crud.py** com as funções CRUD, onde não há a necessidade de utiilzar o ORM e estrutura MVC citada anteriormente.
