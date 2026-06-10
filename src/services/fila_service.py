```python
# Importa a biblioteca 're', usada para trabalhar com expressões regulares
# (validação de formatos como nome, telefone, email, etc.)
import re

# Importa a variável 'fila', que é uma lista que armazena pacientes em espera
from src.data.fila import fila

# Importa funções para manipulação do banco de dados:
# - fechar_conexao: encerra a conexão com o banco
# - obter_conexao: cria/retorna uma conexão com o banco
from src.config.database import fechar_conexao, obter_conexao

# Importa uma função utilitária que lê um número inteiro dentro de um intervalo específico
# (evita erro de digitação do usuário)
from src.utils.input_utils import ler_inteiro_entre


# Lista com os possíveis status de um chamado (usado para controle do fluxo)
STATUS_CHAMADOS = ["Aberta", "Em andamento", "Fechada"]


# Função que calcula a média entre impacto e urgência
# Isso é usado para definir a prioridade do chamado
def calcular_media(impacto, urgencia):
    return (impacto + urgencia) / 2


# Define a prioridade com base na média calculada
# Regras de negócio:
# >= 4 → Alta
# >= 2.5 → Média
# < 2.5 → Baixa
def definir_prioridade(media):
    if media >= 4:
        return 'Alta'

    if media >= 2.5:
        return 'Media'

    return 'Baixa'


# Busca um paciente pelo nome no banco
# Se existir → retorna o ID
# Se NÃO existir → cria um novo paciente e retorna o ID criado
def obter_ou_criar_paciente(cursor, nome, data_nascimento=None, telefone=None, email=None):
    
    # Executa uma query para buscar o paciente pelo nome
    cursor.execute(
        'SELECT id_paciente FROM pacientes WHERE nome = %s LIMIT 1',
        (nome,)
    )
    paciente = cursor.fetchone() # Retorna APENAS UM resultado

    # Se encontrou o paciente, retorna o ID dele
    if paciente:
        return paciente[0]

    # Caso não exista, insere no banco
    cursor.execute(
        """
        INSERT INTO pacientes (nome, data_nascimento, telefone, email)
        VALUES (%s, %s, %s, %s)
        """,
        (nome, data_nascimento, telefone, email)
    )

    # Retorna o ID do último registro inserido
    return cursor.lastrowid #pega o ID que o banco acabou de criar, último ID


# Busca um médico pelo nome
def obter_medico_por_nome(cursor, nome_medico):
    cursor.execute(
        """
        SELECT id_medico
        FROM medicos
        WHERE nome = %s
        LIMIT 1
        """,
        (nome_medico,)
    )
    medico = cursor.fetchone()

    # Se encontrou, retorna ID
    if medico:
        return medico[0]

    # Se não encontrou, retorna None
    return None


# Busca TODOS os médicos cadastrados
def _buscar_medicos(cursor):
    cursor.execute(
        """
        SELECT id_medico, crm, nome, especialidade
        FROM medicos
        ORDER BY nome
        """
    )
    return cursor.fetchall() #retorna todos os resultados


# Procura um paciente pelo nome dentro da fila (lista em memória)
# Retorna o índice do paciente na fila
def obter_indice_paciente_por_nome(nome_paciente):
    for i, paciente in enumerate(fila):
        if paciente[0].lower() == nome_paciente.lower():
            return i

    return None


# Função para adicionar paciente (entrada de dados + validação + banco)
def adicionar_paciente():
    print("Digite 0 em qualquer campo para cancelar.\n")

    # Validação do nome
    while True:
        nome = input("Nome do paciente: ").strip()

        # Permite cancelar operação
        if nome == "0":
            print("Operação cancelada.\n")
            return

        # Não permite vazio
        if nome == "":
            print("Nome não pode ser vazio.\n")
            continue

        # Regex: aceita apenas letras e espaços
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', nome):
            print("Nome deve conter apenas letras.\n")
            continue

        break


    # Validação da data de nascimento
    while True:
        data_str = input("Data de nascimento (AAAAMMDD): ").strip()

        if data_str == "0":
            return

        # Deve ter exatamente 8 números
        if not re.match(r'^\d{8}$', data_str):
            continue

        # Extrai mês e dia
        mes = int(data_str[4:6])
        dia = int(data_str[6:8])

        # Validação simples de data
        if not (1 <= mes <= 12 and 1 <= dia <= 31):
            continue

        # Formata para padrão SQL
        data_nascimento = f"{data_str[:4]}-{data_str[4:6]}-{data_str[6:8]}"
        break


    # Validação de telefone
    while True:
        telefone = input("Telefone do paciente: ").strip()

        if telefone == "0":
            return

        # Regex aceita números, (), -, espaço
        if not re.match(r'^[\d()\-\s]+$', telefone):
            continue

        # Remove caracteres não numéricos
        digitos = re.sub(r'\D', '', telefone)

        # Formata telefone automaticamente
        if len(digitos) == 10:
            telefone = f"({digitos[:2]}) {digitos[2:6]}-{digitos[6:]}"
        elif len(digitos) == 11:
            telefone = f"({digitos[:2]}) {digitos[2:7]}-{digitos[7:]}"
        else:
            continue

        break


    # Validação de email
    while True:
        email = input("Email do paciente: ").strip()

        if email == "0":
            return

        # Regex simples para email
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            continue

        break


    # Abre conexão com banco
    conexao = obter_conexao()

    if conexao is None:
        return

    try:
        cursor = conexao.cursor()

        # Insere paciente no banco
        cursor.execute(
            """
            INSERT INTO pacientes (nome, data_nascimento, telefone, email)
            VALUES (%s, %s, %s, %s)
            """,
            (nome, data_nascimento, telefone, email)
        )

        conexao.commit()

    except Exception as erro:
        conexao.rollback() #Desfaz tudo que foi feito na transação atual em caso de erro
        print(erro)
        return

    finally:
        cursor.close()
        fechar_conexao(conexao)


    # Adiciona paciente também na fila (memória)
    fila.append([nome, data_nascimento, telefone, email])

    print(f"Paciente '{nome}' adicionado.\n")


# Remove o primeiro paciente da fila (FIFO - fila real)
def chamar_proximo():
    if not fila:
        print("Não há pacientes na fila.\n")
        return

    # Remove o primeiro da lista
    paciente = fila.pop(0)
    nome = paciente[0]

    print(f"Chamando: {nome}")


# Mostra a fila atual
def ver_fila():
    if not fila:
        print("Fila vazia.\n")
        return

    for paciente in fila:
        print(paciente[0])


# Função principal de menu
def mostrar_menu():
    print("===== SISTEMA HOSPITALAR =====")
    print("1 - Adicionar paciente")
    print("2 - Chamar próximo paciente")
    print("3 - Adicionar Médico")
    print("3 - Ver fila")  # (Aqui tem um pequeno erro: repetiu número 3)
    print("4 - Criar chamado")
    print("0 - Sair")
    print("==============================\n")
```
