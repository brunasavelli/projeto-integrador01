# Sistema de Fila Hospitalar

Projeto para chamar os pacientes de um hospital em python

## Sobre o Projeto: 
Sistema de fila Hospitalar tem como objetivo adicionar e organizar um hospital e os seus pacientes,
usando como base para isso a prioridade de impacto e urgência, assim descobrindo os primeiros que devem ser atendidos.

**Problema que resolve:** Dificuldade em fazer uma ordem das pessoas que vão comparecendo, sendo que as vezes uma,
pessoa com menos urgência é atendida primeiro que uma com risco de morte até.

### O sistema realiza:
  * Cadastro de pacientes
  * Controle de prioridade
  * Chamada automática
  * Organização da fila
  * Integração com banco de dados


### Funcionalidades:
  * Adicionar pacientes
  * Definir impacto
  * Definir urgência
  * Visualizar fila
  * Chamar próximo paciente
  * Armazenamento em banco de dados

----

## Regra de Prioridade: 
O critério para descobrir os primeiros pacientes a serem chamados, é a média entre o impacto e a
urgência logo será: média = (impacto + urgencia) / 2. <br>
Dessa forma é organizado o atendimento, em casos que o resultado
da média for igual será levado em consideração o paciente de maior urgência.

----

## Tecnologias Utilizadas:
  * Python
  * MySQL
  * SQL
  * JavaScript

## Arquitetura do Sistema:

├── main.py<br>
├── funcoes.py<br>
├── README.md<br>

├── database/<br>
│   ├── banco.sql<br>
│   └── conexao.py<br>

└── docs/<br>
    ├── documentacao_codigo.md<br>
    ├── documentacao_banco.md<br>
    └── documentacao_conexao.md

## Como Executar:

*1-* Baixe os arquivos do projeto pelo GitHub.

*2-* Abra a pasta do projeto pelo seu editor de código de preferencia

*3-* Execute o script do banco de dados no MySQL:

- database/banco.sql

*4-* Verifique as informações da conexão no arquivo:

- database/conexao.py

*5-* Instale as bibliotecas necessárias:

```bash
pip install mysql-connector-python
```

*6-* Execute o arquivo principal:

```bash
python main.py
```

----

## Documentação do Código:

**main.py:** <br>
É responsável pelo menu pricipal do código e a execução do sistema.

**funçoes.py:** <br>
É responsável pelas funções do sistema.

### Funções:
 * Adicionar pacientes
 * Chamar proximo paciente
 * Inserir médico
 * Visualizar fila


## Documentação do Banco de Dados 

O sistema usa o MySQL.

### Tabelas:
 * Médico
 * Pacientes 
 * Chamados

### Objetivo:
É armazenar as informações do sistema hospitalar.


## Documentação da Conexão
A conexão com o banco de dados é feita atráves da biblioteca mysql.connector.

**Arquivo responsável:** <br>
database/conexao.py

