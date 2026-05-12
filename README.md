# Sistema de fila Hospitalar

Projeto para chamar os pacientes de um hospital em python

# Sobre o projeto: Sistema de fila Hospitalar tem como objetivo adicionar e organizar um hospital e os seus pacientes,
usando como base para isso a prioridade de impacto e urgencia, assim descobrindo os primeiros que devem ser atendidos.

**Problema que resolve:** Dificuldade em fazer uma ordem das pessoas que vão comparecendo, sendo que as vezes uma,
pessoa com menos urgência é atendida primeiro que uma com risco de morte até.

# O sistema realiza:
  Cadastro de pacientes
  Controle de prioridade
  Chamada automática
  Organização da fila
  Integração com banco de dados

----

# Funcionalidades:
  Adicionar pacientes
  Definir impacto
  Definir urgência
  Visualizar fila
  Chamar próximo paciente
  Armazenamento em banco de dados

----

# Regra de prioridade: o criterio para descobrir os primeiros pacientes a serem chamados é a média entre o impacto e a,
urgência logo será: media = (impacto + urgencia) / 2. Dessa forma é organizado o atendimento, em casos que o resultado
da média for igual será levado em consideração o paciente de maior urgência.

# Tecnologias utilizadas:
  -Python
  -Mysql
  -SQL

# Arquitetura do Sistema:

├── main.py
├── funcoes.py
├── README.md

├── database/
│   ├── banco.sql
│   └── conexao.py

└── docs/
    ├── documentacao_codigo.md
    ├── documentacao_banco.md
    └── documentacao_conexao.md

# Como Executar:

1 Baixe os arquivos do projeto pelo GitHub.

2 Abra a pasta do projeto pelo seu editor de código de preferencia

3 Execute o script do banco de dados no MySQL:

database/banco.sql

4 Verifique as informações da conexão no arquivo:

database/conexao.py

5 Instale as bibliotecas necessárias:

```bash
pip install mysql-connector-python
```

6 Execute o arquivo principal:

```bash
python main.py
```


# Documentação do Código:

main.py:
É responsável pelo menu pricipal do código e a execução do sistema.

funçoes.py:
É responsável pelas funções do sistema.

Funções:
 adicionar pacientes
 chamar proximo paciente
 inserir médico
 visualizar fila


# Documentação do Banco de dados 

o sistema usa o MySQL.

Tabelas:
 médico
 pacientes 
 chamdos

Objetivo:
É armazenar as informações do sistema hospitalar.


# Documentação da conexão

A conexão com o banco de dados é feita atráves da biblioteca mysql.connector.

Arquivo responsável:
database/conexao.py

