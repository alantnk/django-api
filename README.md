# CRM em Django

Este projeto tem como objetivo construir um CRM simples utilizando Django. O sistema é voltado para o gerenciamento básico de clientes, oportunidades de vendas, tarefas e relatórios, permitindo que os usuários possam visualizar e gerenciar essas informações de maneira prática e intuitiva.

## Funcionalidades

#### 1. Cadastro e Gestão de Clientes

-   **Adicionar Cliente**: Cadastro de informações como nome, e-mail, telefone, e endereço.
-   **Listar Clientes**: Visualizar todos os clientes cadastrados.
-   **Editar Cliente**: Alterar as informações de um cliente existente.
-   **Excluir Cliente**: Remover um cliente do sistema.
-   **Gerenciar Contatos**: Registrar detalhes sobre os contatos realizados com os clientes, como telefone, e-mail, e data do último contato.

#### 2. Gestão de Oportunidades de Vendas

-   **Cadastrar Oportunidade**: Criar uma nova oportunidade de venda para um cliente, com informações sobre valor, estágio da venda, e data de fechamento.
-   **Visualizar Oportunidades**: Exibir todas as oportunidades de vendas registradas.
-   **Alterar Estágio**: Alterar o estágio da oportunidade (ex: 'Prospecção', 'Negociação', 'Fechada').
-   **Histórico de Oportunidades**: Registrar e exibir mudanças de status e atualizações em uma oportunidade.

#### 3. Tarefas e Atividades

-   **Adicionar Tarefa**: Criar tarefas relacionadas aos clientes ou às oportunidades (ex: telefonemas, reuniões, follow-ups).
-   **Listar Tarefas**: Visualizar todas as tarefas pendentes.
-   **Marcar Tarefa como Concluída**: Atualizar o status das tarefas à medida que forem concluídas.
-   **Atribuir Data de Vencimento**: Definir datas para o cumprimento das tarefas.

#### 4. Relatórios Básicos

-   **Dashboard**: Painel de controle com métricas básicas como o total de vendas fechadas, número de oportunidades em cada estágio, e tarefas pendentes.
-   **Relatórios de Vendas**: Exibir o valor total das vendas realizadas e as oportunidades que estão em aberto.

#### 5. Gestão de Usuários

-   **Cadastro de Usuários**: Cadastro de usuários com diferentes permissões (administrador, representante de vendas).
-   **Permissões**: Controle de permissões para cada tipo de usuário, definindo quem pode visualizar ou editar determinadas informações.

## Estrutura do Projeto

O projeto será dividido em cinco principais **partes**:

#### 1. `clients`

-   Modelos: `Client`, `Contact`
-   Funcionalidades: Cadastro e gerenciamento de clientes, além de registros de contatos.

#### 2. `sales`

-   Modelos: `Sale`, `SaleHistory`
-   Funcionalidades: Gerenciamento de oportunidades de vendas, incluindo a criação e atualização de estágios.

#### 3. `tasks`

-   Modelos: `Task`, `Tag`
-   Funcionalidades: Gerenciamento de tarefas relacionadas aos clientes e oportunidades, com vencimento e status de conclusão.

#### 5. `user_control` (_app_)

-   Modelos: `User`
-   Funcionalidades: Gerenciamento de usuários e permissões no sistema.

## Instalação e uso

#### 1. Clone o repositório

```bash
$ git clone https://github.com/alant2031/melo-crm-backend.git
$ cd melo-crm-backend
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
(.venv) $ pip install -r requirements.txt
```

#### 4. Migrations

Renomeie o arquivo `.env-example` para `.env` e execute as migrations

```bash
(.venv) $ python3 manage.py migrate
```

#### 5 Iniciar servidor

Primeiro crie um usuário com o comando `python3 manage.py createsuperuser`.

Preencha os campos e depois inicie o servidor

```bash
(.venv) $ python3 manage.py runserver
```

Acesse o endereço base http://127.0.0.1:8000 e leia a documentação.

#### 6 Seeds (Opcional)

Para pre-popular o banco abra o **shell** do Django com `python3 manage.py shell`

```py
from core.tests import make_data
make_data()
```

Depois feche o terminal e rode o servidor novamente

## Tests

```bash
(.venv) $ python3 manage.py test
```

Ou execute `pytest`

#### HTTP Client(Insomnia)

Caso use o Insomnia, importe o arquivo **melo_api.json**
