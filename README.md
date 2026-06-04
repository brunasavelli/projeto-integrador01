# Sistema de Fila Hospitalar

Projeto em Python para gerenciar pacientes, médicos e chamados em um sistema hospitalar.

## Sobre o Projeto: 
O Sistema de Fila Hospitalar tem como objetivo cadastrar pacientes, registrar médicos e controlar chamados hospitalares com base na urgência e no impacto informados para cada paciente.

A prioridade é calculada usando a média entre impacto e urgência, ajudando a identificar quais casos precisam de mais atenção.

**Problema que resolve:** Ajuda a organizar atendimentos hospitalares, evitando que pacientes com maior urgência sejam deixados para depois.

### O sistema realiza:
  * Cadastro de pacientes
  * Cadastro de médicos
  * Criação de chamados
  * Listagem de pacientes
  * Visualização de chamados
  * Filtro de chamados por status
  * Filtro de chamados por prioridade
  * Atualização do status dos chamados
  * Integração com banco de dados MySQL


### Funcionalidades:
  * Adicionar pacientes
  * Definir impacto
  * Definir urgência
  * Calcular prioridade
  * Abrir chamado
  * Ver chamados
  * Iniciar chamado
  * Finalizar chamado
  * Adicionar médico
  * Listar pacientes
  * Armazenar dados no banco de dados


----

## Regra de Prioridade: 
O critério usado para definir a prioridade do paciente é a média entre impacto e urgência:

```python
media = (impacto + urgencia) / 2
```
A prioridade é definida assim:
 * Média maior ou igual a 4: Alta
 * Média maior ou igual a 2.5: Média
 * Média menor que 2.5: Baixa

Também existe uma função para chamar o próximo paciente da fila. Nela, o paciente com maior média é chamado primeiro. Em caso de empate, é chamado o paciente com maior urgência.

----

## Tecnologias Utilizadas:
  * Python
  * MySQL
  * SQL
  * mysql-connector-python
  * python-dotenv

## Arquitetura do Sistema:

```text
projeto-integrador01/
├── README.md
├── requirements.txt
├── .env
└── codigo/
    ├── main.py
    └── src/
        ├── config/
        │   └── database.py
        ├── data/
        │   └── fila.py
        ├── services/
        │   └── fila_service.py
        ├── utils/
        │   └── input_utils.py
        └── banco_de_dados/
            ├── pacientes.sql
            ├── medicos.sql
            └── chamados.sql
```

## Como Executar:

*1-* Baixe os arquivos do projeto pelo GitHub.

*2-* Abra a pasta do projeto pelo seu editor de código de preferência

*3-* Crie o banco de dados no MySQL:

    CREATE DATABASE hospital_db;

*4-* Execute os scripts SQL dentro da pasta banco_de_dados:

banco_de_dados/pacientes.sql <br>
banco_de_dados/medicos.sql<br>
banco_de_dados/chamados.sql<br>

*5-* Configure o arquivo .env com os dados da conexão: 

HOST=localhost<br>
USER=seu_usuario<br>
PASSWORD=sua_senha<br>
NAME=hospital_db<br>

*6-* Instale as bibliotecas necessárias: 
```bash
pip install -r requirements.txt
```
*7-* Execute o arquivo principal: 
```bash
python codigo/main.py
```

----

## Documentação do Código:

**codigo/main.py:** <br>
É responsável pelo menu principal e pela execução do sistema.

O menu possui as opções:

* Cadastrar paciente
* Abrir chamado
* Ver chamados
* Iniciar chamado
* Finalizar chamado
* Adicionar médico
* Listar pacientes
* Sair

**src/services/fila_service.py:** <br>
Contém as principais regras e funções do sistema, como:

* Calcular média
* Definir prioridade
* Adicionar paciente
* Adicionar médico
* Criar chamado
* Ver chamados
* Iniciar chamado
* Finalizar chamado
* Listar pacientes
* Chamar próximo paciente
* Ver fila

**src/data/fila.py:** <br>
Armazena a fila temporária de pacientes em uma lista Python.

**src/config/database.py:** <br>
Responsável por abrir e fechar a conexão com o banco de dados MySQL usando a biblioteca mysql.connector.

**srvc/utils/input_utils.py:** <br>
Contém função auxiliar para validar entrada de números inteiros dentro de um intervalo.


## Documentação do Banco de Dados 

O sistema usa o MySQL.

### Tabelas
* pacientes
* medicos
* chamados

### Tabela pacientes
Armazena os dados dos pacientes:
* ID
* Nome
* Data de nascimento
* Telefone
* Email

### Tabela medicos
Armazena os dados dos médicos:
* ID
* CRM
* Nome
* Especialidade

### Tabela chamados
Armazena os chamados criados no sistema:
* ID do chamado
* Paciente
* Médico
* Descrição
* Urgência
* Prioridade
* Status
* Data de abertura


## Documentação da Conexão:
A conexão com o banco de dados é feita através da biblioteca mysql.connector.

O arquivo responsável pela conexão é: <br>
src/config/database.py

As informações de conexão são lidas do arquivo .env.