```python
# Importa o módulo mysql.connector
# Ele é responsável por permitir que o Python se conecte a um banco de dados MySQL
import mysql.connector

# Importa a função load_dotenv da biblioteca dotenv
# Essa função carrega variáveis de ambiente de um arquivo .env
from dotenv import load_dotenv

# Importa o módulo os, que permite acessar variáveis do sistema (como variáveis de ambiente)
import os


# Carrega as variáveis do arquivo .env para dentro do programa
# override=True permite sobrescrever variáveis que já existam no ambiente
# Exemplo: HOST, USER, PASSWORD, NAME
load_dotenv(override=True)


# Função responsável por CRIAR e RETORNAR uma conexão com o banco de dados
def obter_conexao():

    try:
        # Tenta estabelecer conexão com o banco MySQL
        # mysql.connector.connect() cria uma conexão ativa com o banco
        
        conexao = mysql.connector.connect(

            # host → endereço do servidor do banco (ex: localhost ou IP)
            # os.getenv("HOST") pega essa informação do arquivo .env
            host=os.getenv("HOST"),

            # user → usuário do banco de dados
            # necessário para autenticação
            user=os.getenv("USER"),

            # password → senha do banco
            # garante segurança na conexão
            password=os.getenv("PASSWORD"),

            # database → nome do banco que será utilizado
            # é onde estão as tabelas (pacientes, médicos, chamados, etc.)
            database=os.getenv("NAME")
        )

        # Se a conexão foi bem sucedida, retorna o objeto de conexão
        # Esse objeto será usado depois para executar comandos SQL
        return conexao

    except Exception as erro:
        # Se acontecer qualquer erro (ex: senha errada, banco offline, etc.)

        print("Erro ao conectar:")
        print(erro)

        # Retorna None para indicar que a conexão falhou
        # Isso é importante para evitar que o sistema quebre depois
        return None


# Função responsável por FECHAR a conexão com o banco de dados
def fechar_conexao(conexao):

    try:
        # Verifica se a conexão existe (não é None)
        # Isso evita erro caso tente fechar uma conexão inexistente
        if conexao:

            # Fecha a conexão com o banco
            # Isso libera recursos e evita sobrecarga no banco
            conexao.close()

    except Exception as erro:
        # Caso ocorra erro ao fechar a conexão

        print("Erro ao fechar conexão:")
        print(erro)
```
