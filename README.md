# Library Management System

## Descrição

Este projeto é um sistema de Gerenciamento de Biblioteca, criado para praticar conceitos de Programação Orientada a Objetos (POO) e o padrão arquitetural MVC (Model-View-Controller). O sistema está estruturado em módulos e segue uma abordagem escalável, com funcionalidades de CRUD para gerenciar livros e usuários.

Nesta primeira release (v1.0.0), o projeto contém uma interface de console com funcionalidades básicas e cobertura de testes unitários para os controllers. Melhorias futuras estão planejadas em releases seguintes.

## Melhorias Programadas

As próximas etapas do projeto incluem:

1. **Banco de Dados**: Integração de um banco de dados relacional (PostgreSQL ou MySQL) para armazenar os dados persistentes de livros e usuários.
2. **Interface Web**: Migração para Django, transformando o sistema em uma aplicação web com templates HTML.
3. **APIs REST**: Implementação de uma API REST com Django Rest Framework, possibilitando integração com outras aplicações.
4. **Validações de Dados**: Melhorias nas validações de campos de entrada, garantindo formatos corretos (e.g., ISBN válido, formato de email).
5. **Melhorias na Interface**: Na próxima release, a interação do usuário será otimizada com a interface web.

### Principais componentes:

- **Modelos**: Representação dos dados de Livros e Usuários.
- **Controllers**: Lógica de negócios para gerenciar as operações com Livros e Usuários.
- **Views**: Interface de console para coleta de dados e exibição de informações.
- **Main**: Ponto de entrada do sistema, que gerencia a navegação no menu e a chamada das funcionalidades.

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

### Testes Unitários

Os controllers possuem cobertura de testes unitários com **pytest**, utilizando boas práticas como a inicialização de fixtures para garantir que os livros e usuários estejam cadastrados antes dos testes. A cobertura de código foi verificada com a ferramenta **pytest-cov**, garantindo uma boa robustez do sistema.

## Estrutura do Projeto

- **`models.py`**: Define as classes `Book` e `User`, que representam os dados da aplicação.
- **`controllers.py`**: Contém as classes `BookController` e `UserController`, responsáveis pela lógica de negócio e manipulação dos dados.
- **`views.py`**: Responsável pela interface de usuário (UI) no console, interagindo com os controllers.
- **`main.py`**: Controla o fluxo principal do programa, gerenciando o menu e as opções de navegação.
- **`test_controllers.py`**: Contém os testes unitários dos controllers, verificando a integridade das funcionalidades de CRUD.

## Exemplo de Uso

Ao executar o programa, será exibido um menu principal no terminal, onde você pode gerenciar **livros** ou **usuários**. Cada opção oferece as operações de CRUD necessárias.

```bash
$ python main.py

- Type 1 to manage books.
- Type 2 to manage users.
- Type 0 "zero" to exit system.
--------------------------------------------------
```

## Requisitos

- Python 3.x
- Biblioteca `prompt_toolkit` para melhorar a interface de entrada no terminal.

## Como Rodar o Projeto

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/library-management.git
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute o programa:

```bash
python main.py
```

## Contribuições

Contribuições são bem-vindas! Se você quiser sugerir melhorias ou funcionalidades, sinta-se à vontade para abrir uma issue ou enviar um pull request.
