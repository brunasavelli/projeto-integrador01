from src.config.database import fechar_conexao, obter_conexao
from src.data.fila import fila
from src.utils.input_utils import ler_inteiro_entre

def calcular_media(impacto, urgencia):
    return (impacto + urgencia) / 2


def adicionar_paciente():
    #tenta abrir a conexão com o banco de dados
    conexao = obter_conexao()

    #se não conseguir conectar para a função
    if conexao is None:
        return None

    try:
        #cria um "cursor" que é o objeto usado para executar comandos sql
        cursor = conexao.cursor()

        #comando sql para inserir o paciente da tabela
        sql = """
        INSERT INTO pacientes (nome, data_nascimento, telefone, email)
        VALUES ('ana', '19-05-2008', '(19)98855-2233', 'ana@gmail.com')
        """

        #executa o comando sql no banco
        cursor.execute(sql)

        #salva (confirma) a altração no banco
        conexao.commit()

        #retorna o ID do ultimo registro inserido 
        return cursor.lastrowid  

    except Exception as erro:
        #se encontrar algum erro, mostra na tela
        print("Erro:", erro)

        #fecha o cursor
        cursor.close()

        #fecha a conexao com o banco
        fechar_conexao(conexao)

        #retorna none indicando que deu erro
        return None
    
       


def chamar_proximo():
    if not fila:
        print("ℹ️ Não há pacientes na fila.\n")
        return

    indice_maior = 0

    for i in range(1, len(fila)):

        if fila[i][3] > fila[indice_maior][3]:
            indice_maior = i

        elif fila[i][3] == fila[indice_maior][3]:

            if fila[i][2] > fila[indice_maior][2]:
                indice_maior = i

    paciente = fila.pop(indice_maior)

    nome, impacto, urgencia, media = paciente

    print("\nChamando próximo paciente:\n")
    print(f"Nome: {nome}")
    print(f"Impacto: {impacto}")
    print(f"Urgência: {urgencia}")
    print(f"Média: {media:.1f}\n")


def ver_fila():
    if not fila:
        print("Fila vazia.\n")
        return

    print("\n--- FILA ATUAL ---")

    for nome, impacto, urgencia, media in fila:
        print(
            f"{nome} | "
            f"Urgência: {urgencia} | "
            f"Impacto: {impacto} | "
            f"Média: {media:.1f}"
        )

    print("------------------\n")


def mostrar_menu():
    print("===== SISTEMA HOSPITALAR =====")
    print("1 - Adicionar paciente")
    print("2 - Chamar próximo paciente")
    print("3 - Ver fila")
    print("0 - Sair")
    print("==============================\n")
