# Library Management System

## Descrição

Este projeto é um sistema simples de gerenciamento de biblioteca, desenvolvido para praticar conceitos de Programação Orientada a Objetos (POO) e o padrão arquitetural MVC (Model-View-Controller). O objetivo é criar um sistema modular e escalável, começando com funcionalidades básicas de CRUD (Create, Read, Update, Delete) para gerenciar livros e usuários, com melhorias progressivas planejadas.

Atualmente, o projeto possui:

- **Modelos**: Representação dos dados de Livros e Usuários.
- **Controllers**: Lógica de negócios para gerenciar as operações com Livros e Usuários.
- **Views**: Interface de console que coleta os dados dos usuários e exibe as informações.
- **Main**: Arquivo principal que inicializa o menu de navegação e as funcionalidades.

## Funcionalidades Atuais

### Gerenciamento de Livros

- Adicionar novos livros
- Listar todos os livros cadastrados
- Pesquisar livro por código ISBN
- Atualizar informações de um livro
- Excluir um livro do sistema

### Gerenciamento de Usuários

- Registrar novos usuários
- Listar todos os usuários cadastrados
- Pesquisar usuário por código
- Atualizar informações de um usuário
- Excluir um usuário do sistema

## Estrutura do Projeto

- **`models.py`**: Contém as classes `Book` e `User`, que representam os modelos de dados.
- **`controllers.py`**: Inclui as classes `BookController` e `UserController`, responsáveis pela lógica de negócios e manipulação dos dados.
- **`views.py`**: Responsável pela interface de usuário (UI), coletando dados e interagindo com os controllers.
- **`main.py`**: Ponto de entrada do sistema, que controla o fluxo do programa e chama as funções de view e controller.

## Exemplo de Uso

Ao executar o programa, será exibido um menu principal no terminal, onde você pode escolher gerenciar **livros** ou **usuários**. Cada opção apresenta funcionalidades como **adicionar**, **listar**, **buscar**, **atualizar** ou **excluir** os dados.

```bash
$ python main.py

- Type 1 to manage books.
- Type 2 to manage users.
- Type 0 "zero" to exit system.
--------------------------------------------------
```

Ao escolher uma das opções (1 ou 2), o sistema permitirá que você realize as operações de CRUD correspondentes.

## Escalabilidade e Melhorias Futuras

Este projeto será expandido com as seguintes melhorias:

1. **Validações de Dados**: Implementação de validações nos campos de entrada para garantir que os dados estejam no formato correto (e.g., ISBN válido, email formatado corretamente).
2. **Persistência de Dados**: Implementação de um banco de dados relacional (provavelmente PostgreSQL ou MySQL) para armazenar os dados de livros e usuários.
3. **Testes Unitários**: Criação de testes unitários para garantir a integridade das funcionalidades e evitar regressões.
4. **API REST**: Evoluir o sistema para uma API REST utilizando Django Rest Framework (DRF), permitindo a comunicação via HTTP e possibilitando a criação de interfaces web e mobile.
5. **Interface Web**: Implementação de uma interface web com Django, para fornecer uma UI mais moderna e acessível.

## Requisitos

- Python 3.x
- Biblioteca `prompt_toolkit` para melhorar a interface de entrada de dados no terminal

## Como Rodar o Projeto

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/biblioteca-management.git
```

2. Instale as dependências:

```bash
pip install prompt_toolkit
```

3. Execute o programa:

```bash
python main.py
```

## Contribuições

Contribuições são bem-vindas! Se você quiser sugerir melhorias ou novas funcionalidades, fique à vontade para abrir uma issue ou enviar um pull request.
