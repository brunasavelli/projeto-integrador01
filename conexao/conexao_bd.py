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

#def insercao_de_aluno (ra, nome): #cria a função de inserção de alunos
#    comando = f"insert into Alunos (RA, Nome) values ({ra}, '{nome}')" #insere um aluno novo na tabela
#    conexao = obtemConexao("172.16.12.14", "BD240226129", "Izfoa7", "BD240226129") #chama a função de conexao e passa os parametros esperados
#    cursor = conexao.cursor() #escreve o aluno novo no banco
#    cursor.execute(comando) #execudar o comando do insert
#    conexao.commit() #salva no banco de dados

#insercao_de_aluno(12345678, "cleiton") #insere o aluno

# Função para inserir um médico na tabela "medicos"
def inserir_medico(nome, especialidade):
    comando = f"INSERT INTO medicos (nome, especialidade) VALUES ('{nome}', '{especialidade}')"# Comando SQL para inserir um médico
    conexao = obtemConexao("172.16.12.14", "BD240226129", "Izfoa7", "BD240226129")# Obtém a conexão com o banco
    cursor = conexao.cursor()# Cria um cursor (objeto que executa comandos SQL)
    cursor.execute(comando)# Executa o comando SQL com os valores informados
    conexao.commit()# Confirma a operação (salva no banco de dados)
    print("Médico inserido com sucesso!")# Mensagem de confirmação


# Função para inserir um paciente na tabela "pacientes"
def inserir_paciente(nome, data_nascimento, telefone, email):
    comando = f" INSERT INTO pacientes (nome, data_nascimento, telefone, email) VALUES ('{nome}', '{data_nascimento}', '{telefone}', '{email}')"# Comando SQL para inserir um paciente
    conexao = obtemConexao("172.16.12.14", "BD240226129", "Izfoa7", "BD240226129") # Obtém a conexão com o banco
    cursor = conexao.cursor()# Cria o cursor para executar comandos SQL
    cursor.execute(comando)# Executa o comando SQL
    conexao.commit()# Salva no banco
    print("Paciente inserido com sucesso!") # Mensagem de confirmação


# Função para inserir um chamado na tabela "chamados"
def inserir_chamado(id_paciente, id_medico, descricao, urgencia, prioridade):
    comando = f"INSERT INTO chamados (id_paciente, id_medico, descricao, urgencia, prioridade) VALUES ({id_paciente}, {id_medico}, '{descricao}', {urgencia}, '{prioridade}')" #Comando SQL para inserir um chamado
    conexao = obtemConexao("172.16.12.14", "BD240226129", "Izfoa7", "BD240226129")# Obtém a conexão com o banco
    cursor = conexao.cursor()# Cria o cursor
    cursor.execute(comando)# Executa o comando SQL
    conexao.commit() # Confirma a inserção
    print("Chamado inserido com sucesso!")# Mensagem de sucesso

# =========================
# EXEMPLOS DE EXECUÇÃO
# =========================

inserir_medico("Fábio Silva", "Cardiologia")# Insere um médico na tabela

inserir_paciente("Maria Oliveira", "1985-07-15", "11987654321", "maria@email.com")# Insere um paciente
 
inserir_chamado(1, 1, "Paciente com dor no peito", 5, "Alta")# Insere um chamado relacionando paciente e médico, (os IDs precisam existir no banco)