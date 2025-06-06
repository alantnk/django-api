# CRM em Django

Este projeto tem como objetivo construir um CRM simples utilizando Django. O sistema é voltado para o gerenciamento básico de clientes, oportunidades de vendas, tarefas e relatórios, permitindo que os usuários possam visualizar e gerenciar essas informações de maneira prática e intuitiva.


## Estrutura do Projeto

O projeto será dividido em quatro **partes**:

#### 1. `clients`

-   Modelos: `Client`, `Contact`
-   Funcionalidades: Cadastro e gerenciamento de clientes, além de registros de contatos.

#### 2. `sales`

-   Modelos: `Sale`, `SaleHistory`
-   Funcionalidades: Gerenciamento de oportunidades de vendas, incluindo a criação e atualização de estágios.

#### 3. `tasks`

-   Modelos: `Task`, `Tag`
-   Funcionalidades: Gerenciamento de tarefas relacionadas aos clientes e oportunidades, com vencimento e status de conclusão.

#### 4. `user_control` (_app_)

-   Modelos: `User`
-   Funcionalidades: Gerenciamento de usuários e permissões no sistema.

## Instalação e uso

#### 1. Clone o repositório

```bash
$ git clone git@github.com:alantnk/django-api.git
$ cd django-api
```

#### 2. Ambiente virtual

Crie e ative o ambiente

```bash
$ virtualenv .venv
$ source .venv/bin/activate
```

**Veja:** [**Como instalar virtualenv no Linux e Windows**](https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/)

#### 3. Instalação

Execute a instalação dos pacotes

```bash
$ pip install -r requirements.txt
```

#### 4. Migrations

Renomeie o arquivo `.env-example` para `.env` e execute as migrations

```bash
$ python3 manage.py migrate
```

#### 5. Iniciar servidor

Primeiro crie um usuário com o comando `python3 manage.py createsuperuser`.

Preencha os campos e depois inicie o servidor

```bash
$ python3 manage.py runserver
```

Acesse o endereço base http://127.0.0.1:8000 e leia a documentação.

#### 6. Seeds (Opcional)

Para pre-popular o banco abra o **shell** do Django com `python3 manage.py shell`

```py
from core.tests import make_data
make_data()
```

Depois feche o terminal e rode o servidor novamente

## Tests

```bash
$ python3 manage.py test
```

Ou execute `pytest`

#### HTTP Client(Insomnia)

Caso use o Insomnia, importe o arquivo **api_collection.json**
