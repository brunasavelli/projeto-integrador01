import mysql.connector #importa a biblioteca mysql.connector

def obtemConexao (servidor, usuario, senha, bd): #cria uma funçao para obter a conexao definindo os parâmetros
    if obtemConexao.conexao==None: #testa se a conexao é vazia
        obtemConexao.conexao = mysql.connector.connect( #se ela for vazia ela recebe os parâmetros abaixo
            host=f"{servidor}",\
            user=f"{usuario}",\
            password=f"{senha}",\
            database=f"{bd}"
        )
    return obtemConexao.conexao #devolve a conexao
obtemConexao.conexao=None #deixa a conexao vazia denovo

def insercao_de_aluno (ra, nome): #cria a função de inserção de alunos
    comando = f"insert into Alunos (RA, Nome) values ({ra}, '{nome}')" #insere um aluno novo na tabela
    conexao = obtemConexao("172.16.12.14", "BD240226129", "Izfoa7", "BD240226129") #chama a função de conexao e passa os parametros esperados
    cursor = conexao.cursor() #escreve o aluno novo no banco
    cursor.execute(comando) #execudar o comando do insert
    conexao.commit() #salva no banco de dados

insercao_de_aluno(12345678, "cleiton") #insere o aluno 