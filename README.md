# Library Management System


## Descrição

Este projeto é um sistema de gerenciamento de biblioteca, desenvolvido inicialmente para praticar conceitos de Programação Orientada a Objetos (POO) e o padrão arquitetural MVC (Model-View-Controller).
O objetivo agora é criar um sistema modular e escalável, com funcionalidades de CRUD para gerenciar livros e usuários, e evoluir gradualmente até um sistema web robusto com APIs REST.
Ao longo do desenvolvimento, o projeto passou por várias melhorias, incluindo a implementação de validações de dados, cobertura total de testes unitários e a integração com um banco de dados PostgreSQL, permitindo a persistência de dados. O foco é criar um sistema que não apenas funcione bem, mas também seja fácil de manter e expandir no futuro.

## Observações Importantes
### Branch Principal: 
O repositório está configurado para utilizar a branch develop como padrão. Para acessar a versão mais estável do projeto, selecione a `branch **main**` ao clonar o repositório.

## Melhorias Implementadas na Release v1.1.0

1. **Persistência de Dados**: Implementação de um banco de dados PostgreSQL para armazenar dados de livros e usuários.
2. **Validações**: Validações robustas nos dados de entrada para garantir a integridade dos registros, incluindo validações numéricas e de formato.
3. **Tratamento de Exceções**: Implementação de um tratamento de erros mais específico para capturar exceções relacionadas ao banco de dados.
4. **Melhorias na Interface de Usuário**: Mesmo rodando apenas no console, agora o sistema conta com uma visualização mais amigável para interação com o usuário.
5. **Melhorias na Estrutura do Código**: O código foi refatorado para seguir boas práticas de programação, com maior modularização e clareza.

## Funcionalidades Atuais

### Gerenciamento de Livros

- Adicionar novos livros com validações de dados
- Listar todos os livros cadastrados
- Pesquisar livro por código ISBN
- Atualizar informações de um livro
- Excluir um livro do sistema

### Gerenciamento de Usuários

- Registrar novos usuários com validações de dados
- Listar todos os usuários cadastrados
- Pesquisar usuário por código
- Atualizar informações de um usuário
- Excluir um usuário do sistema


## Estrutura do Projeto

- **`models.py`**: Contém as classes `Book` e `User`, que representam os modelos de dados.
- **`controllers.py`**: Inclui as classes `BookController` e `UserController`, responsáveis pela lógica de negócios e manipulação dos dados.
- **`views.py`**: Responsável pela interface de usuário (UI), coletando dados e interagindo com os controllers.
- **`main.py`**: Ponto de entrada do sistema, que controla o fluxo do programa e chama as funções de view e controller.
- **`tests/test_controllers_db.py`**: Contém os testes unitários para garantir a funcionalidade do sistema, utilizando a biblioteca `unittest` e `pytest`.

## Estrutura do Banco de Dados

Para que o sistema funcione corretamente, você precisará criar as seguintes tabelas no banco de dados PostgreSQL:

### Tabela `books`

```sql
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    year INTEGER NOT NULL,
    genre VARCHAR(100) NOT NULL,
    isbn_code VARCHAR(20) UNIQUE NOT NULL
);
```

### Tabela `users`

```sql

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(15) NOT NULL,
    user_code INTEGER UNIQUE NOT NULL
);
```

## Acesso ao Banco de Dados

Para que o sistema funcione corretamente, é necessário configurar o acesso ao banco de dados PostgreSQL.

## Criando a Variável de Ambiente para a Senha do Banco de Dados

1. Abra o terminal.
2. Defina a variável de ambiente:
- Para Linux/Mac:

```bash
    export DB_PASSWORD='sua_senha_aqui' 
```
Para Windows:

```bash
    set DB_PASSWORD='sua_senha_aqui'
```
Verifique se a variável foi criada:

```bash
    echo $DB_PASSWORD  # Para Linux/Mac
    echo %DB_PASSWORD%  # Para Windows
```

### Configurando o Banco de Dados

O arquivo db_connection.py é responsável por gerenciar a conexão com o banco de dados PostgreSQL. A configuração padrão é:

```python

import psycopg2
from psycopg2 import sql
import os

db_password = os.getenv('DB_PASSWORD')

def get_connection():
    try:
        conn = psycopg2.connect(
            dbname="library",
            user="postgres",
            password=db_password,
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None
```

## Exemplo de Uso

Ao executar o programa, será exibido um menu principal no terminal, onde você pode escolher gerenciar **livros** ou **usuários**. Cada opção apresenta funcionalidades como **adicionar**, **listar**, **buscar**, **atualizar** ou **excluir** os dados.

```bash
$ python main.py

- Type 1 to manage books.
- Type 2 to manage users.
- Type 0 "zero" to exit system.
--------------------------------------------------
```

## Requisitos

- Python 3.x
- Biblioteca `psycopg2` para acesso ao banco de dados PostgreSQL
- Biblioteca `prompt_toolkit` para melhorar a interface de entrada de dados no terminal
- Biblioteca `tabulate` para exibição de dados em formato de tabela

## Como Rodar o Projeto

1. Clone o repositório `da branch main`

```bash
git clone https://github.com/seu-usuario/library-management.git
```

2. Instale as dependências:

```bash
pip install prompt_toolkit tabulate psycopg2
```

3. Execute o programa:

```bash
python main.py
```

## Contribuições

Contribuições são bem-vindas! Se você quiser sugerir melhorias ou novas funcionalidades, fique à vontade para abrir uma issue ou enviar um pull request.