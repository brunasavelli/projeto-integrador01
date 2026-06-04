import re

from src.data.fila import fila
from src.config.database import fechar_conexao, obter_conexao
from src.utils.input_utils import ler_inteiro_entre


STATUS_CHAMADOS = ["Aberta", "Em andamento", "Fechada"]


def calcular_media(impacto, urgencia):
    return (impacto + urgencia) / 2


def definir_prioridade(media):
    if media >= 4:
        return 'Alta'

    if media >= 2.5:
        return 'Media'

    return 'Baixa'


def obter_ou_criar_paciente(cursor, nome, data_nascimento=None, telefone=None, email=None):
    cursor.execute(
        'SELECT id_paciente FROM pacientes WHERE nome = %s LIMIT 1',
        (nome,)
    )
    paciente = cursor.fetchone()

    if paciente:
        return paciente[0]

    cursor.execute(
        """
        INSERT INTO pacientes (nome, data_nascimento, telefone, email)
        VALUES (%s, %s, %s, %s)
        """,
        (nome, data_nascimento, telefone, email)
    )
    return cursor.lastrowid


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

    if medico:
        return medico[0]

    return None


def _buscar_medicos(cursor):
    cursor.execute(
        """
        SELECT id_medico, crm, nome, especialidade
        FROM medicos
        ORDER BY nome
        """
    )
    return cursor.fetchall()


def obter_indice_paciente_por_nome(nome_paciente):
    for i, paciente in enumerate(fila):
        if paciente[0].lower() == nome_paciente.lower():
            return i

    return None


def adicionar_paciente():
    print("Digite 0 em qualquer campo para cancelar.\n")

    while True:
        nome = input("Nome do paciente: ").strip()
        if nome == "0":
            print("Operação cancelada.\n")
            return
        if nome == "":
            print("Nome não pode ser vazio.\n")
            continue
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', nome):
            print("Nome deve conter apenas letras.\n")
            continue
        break

    while True:
        data_str = input("Data de nascimento (AAAAMMDD): ").strip()
        if data_str == "0":
            print("Operação cancelada.\n")
            return
        if not re.match(r'^\d{8}$', data_str):
            print("Data deve conter exatamente 8 números (ex: 19900525).\n")
            continue
        mes = int(data_str[4:6])
        dia = int(data_str[6:8])
        if not (1 <= mes <= 12 and 1 <= dia <= 31):
            print("Data inválida. Verifique mês (01-12) e dia (01-31).\n")
            continue
        data_nascimento = f"{data_str[:4]}-{data_str[4:6]}-{data_str[6:8]}"
        break

    while True:
        telefone = input("Telefone do paciente (ex: 11987654321 ou (11) 98765-4321): ").strip()
        if telefone == "0":
            print("Operação cancelada.\n")
            return
        if telefone == "":
            print("Telefone não pode ser vazio.\n")
            continue
        if not re.match(r'^[\d()\-\s]+$', telefone):
            print("Telefone deve conter apenas números, parênteses e traço.\n")
            continue
        digitos = re.sub(r'\D', '', telefone)
        if len(digitos) == 10:
            telefone = f"({digitos[:2]}) {digitos[2:6]}-{digitos[6:]}"
        elif len(digitos) == 11:
            telefone = f"({digitos[:2]}) {digitos[2:7]}-{digitos[7:]}"
        else:
            print("Telefone deve ter 10 ou 11 dígitos.\n")
            continue
        break

    while True:
        email = input("Email do paciente: ").strip()
        if email == "0":
            print("Operação cancelada.\n")
            return
        if email == "":
            print("Email não pode ser vazio.\n")
            continue
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            print("Email inválido. Use o formato: nome@dominio.com\n")
            continue
        break

    conexao = obter_conexao()

    if conexao is None:
        print("Não foi possível adicionar paciente: sem conexão com o banco.\n")
        return

    cursor = None

    try:
        cursor = conexao.cursor()
        cursor.execute(
            """
            INSERT INTO pacientes (nome, data_nascimento, telefone, email)
            VALUES (%s, %s, %s, %s)
            """,
            (nome, data_nascimento, telefone, email)
        )
        conexao.commit()

    except Exception as erro:
        conexao.rollback()
        print("Erro ao adicionar paciente no banco de dados:")
        print(erro)
        print()
        return

    finally:
        if cursor:
            cursor.close()

        fechar_conexao(conexao)

    fila.append([nome, data_nascimento, telefone, email])

    print(f"Paciente '{nome}' adicionado.\n")


def adicionar_medico():
    print("Digite 0 em qualquer campo para cancelar.\n")

    crm = input("CRM do medico: ").strip()

    if crm == "0":
        print("Operação cancelada.\n")
        return

    if crm == "":
        print("CRM nao pode ser vazio.\n")
        return

    nome = input("Nome do medico: ").strip()

    if nome == "0":
        print("Operação cancelada.\n")
        return

    if nome == "":
        print("Nome nao pode ser vazio.\n")
        return

    especialidade = input("Especialidade: ").strip()

    if especialidade == "0":
        print("Operação cancelada.\n")
        return

    if especialidade == "":
        print("Especialidade nao pode ser vazia.\n")
        return

    conexao = obter_conexao()

    if conexao is None:
        print("Nao foi possivel adicionar medico: sem conexao com o banco.\n")
        return

    cursor = None

    try:
        cursor = conexao.cursor()
        cursor.execute(
            f"""
            INSERT INTO medicos (crm, nome, especialidade)
            VALUES (%s, %s, %s)
            """,
            (crm, nome, especialidade)
        )
        conexao.commit()

    except Exception as erro:
        conexao.rollback()
        print("Erro ao adicionar medico no banco de dados:")
        print(erro)
        print()
        return

    finally:
        if cursor:
            cursor.close()

        fechar_conexao(conexao)

    print(f"Medico '{nome}' adicionado.\n")


def criar_chamado():
    if not fila:
        print("Não há pacientes na fila para criar um chamado.\n")
        return

    print("\n--- PACIENTES NA FILA ---")
    for i, (nome, *_) in enumerate(fila):
        print(f"{i + 1} - {nome}")
    print("-------------------------\n")

    while True:
        nome_paciente = input("Digite o nome do paciente: ").strip()

        if nome_paciente == "":
            print("Nome do paciente não pode ser vazio.\n")
            continue

        indice = obter_indice_paciente_por_nome(nome_paciente)

        if indice is not None:
            break

        print("Não foi encontrado paciente com esse nome na fila.")
        print("Digite outro nome.\n")

    descricao = input("Descrição do chamado: ").strip()

    if descricao == "":
        print("Descrição não pode ser vazia.\n")
        return

    impacto = ler_inteiro_entre(1, 5, "Impacto (1 a 5): ")
    urgencia = ler_inteiro_entre(1, 5, "Urgência (1 a 5): ")
    media = calcular_media(impacto, urgencia)
    prioridade = definir_prioridade(media)

    nome, data_nascimento, telefone, email = fila[indice][:4]
    conexao = obter_conexao()

    if conexao is None:
        print("Não foi possível criar o chamado: sem conexão com o banco.\n")
        return

    cursor = None

    try:
        cursor = conexao.cursor()
        medicos = _buscar_medicos(cursor)

        if not medicos:
            print("Nenhum medico cadastrado. Cadastre um medico primeiro.\n")
            return

        while True:
            print()
            print("+----+------------+---------------------+---------------+")
            print("| No | CRM        | Medico              | Especialidade |")
            print("+----+------------+---------------------+---------------+")
            for i, (_, crm, nome_medico, especialidade) in enumerate(medicos):
                print(f"| {i + 1:<2} | {crm:<10} | {nome_medico:<19} | {especialidade:<13} |")
            print("+----+------------+---------------------+---------------+")

            indice_medico = ler_inteiro_entre(1, len(medicos), "Selecione o medico: ") - 1
            id_medico = medicos[indice_medico][0]
            break

        id_paciente = obter_ou_criar_paciente(cursor, nome, data_nascimento, telefone, email)

        cursor.execute(
            """
            INSERT INTO chamados (
                id_paciente,
                id_medico,
                descricao,
                urgencia,
                prioridade,
                status
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (id_paciente, id_medico, descricao, urgencia, prioridade, "Aberta")
        )

        conexao.commit()

    except Exception as erro:
        conexao.rollback()
        print("Erro ao criar chamado no banco de dados:")
        print(erro)
        print()
        return

    finally:
        if cursor:
            cursor.close()

        fechar_conexao(conexao)

    if len(fila[indice]) == 4:
        fila[indice].append([])

    fila[indice][4].append(descricao)

    print(f"Chamado criado para '{nome}' com prioridade {prioridade}.\n")


def chamar_proximo():
    if not fila:
        print("Não há pacientes na fila.\n")
        return

    paciente = fila.pop(0)
    nome = paciente[0]

    print("\nChamando próximo paciente:\n")
    print(f"Nome: {nome}\n")


def ver_fila():
    if not fila:
        print("Fila vazia.\n")
        return

    print("\n--- FILA ATUAL ---")

    for paciente in fila:
        nome = paciente[0]
        print(nome)

    print("------------------\n")


def listar_pacientes():
    conexao = obter_conexao()

    if conexao is None:
        print("Nao foi possivel listar os pacientes: sem conexao com o banco.\n")
        return

    cursor = None

    try:
        cursor = conexao.cursor()
        cursor.execute(
            f"""
            SELECT
                id_paciente,
                nome,
                DATE_FORMAT(data_nascimento, '%d/%m/%Y'),
                telefone,
                email
            FROM pacientes
            ORDER BY nome
            """
        )
        pacientes = cursor.fetchall()

    except Exception as erro:
        print("Erro ao buscar pacientes no banco de dados:")
        print(erro)
        print()
        return

    finally:
        if cursor:
            cursor.close()

        fechar_conexao(conexao)

    if not pacientes:
        print("\nNenhum paciente cadastrado.\n")
        return

    print()
    print("+------+----------------------+------------+----------------------+----------------------------+")
    print("| ID   | Nome                 | Nascimento | Telefone             | Email                      |")
    print("+------+----------------------+------------+----------------------+----------------------------+")

    for id_paciente, nome, data_nascimento, telefone, email in pacientes:
        data_nascimento = data_nascimento or ""
        telefone = telefone or ""
        email = email or ""
        print(
            f"| {id_paciente:<4} | "
            f"{nome[:20]:<20} | "
            f"{data_nascimento:<10} | "
            f"{telefone[:20]:<20} | "
            f"{email[:26]:<26} |"
        )

    print("+------+----------------------+------------+----------------------+----------------------------+")
    print()


def ver_chamados():
    print()
    print("+----+-------------------+")
    print("| No | Filtro            |")
    print("+----+-------------------+")
    print("| 1  | Todos             |")
    print("| 2  | Por status        |")
    print("| 3  | Por prioridade    |")
    print("+----+-------------------+")

    opcao_filtro = ler_inteiro_entre(1, 3, "Selecione o filtro: ")
    where = ""
    parametros = ()

    if opcao_filtro == 2:
        print()
        print("+----+---------------+")
        print("| No | Status        |")
        print("+----+---------------+")

        for i, status in enumerate(STATUS_CHAMADOS):
            print(f"| {i + 1:<2} | {status:<13} |")

        print("+----+---------------+")

        indice_status = ler_inteiro_entre(1, len(STATUS_CHAMADOS), "Selecione o status: ") - 1
        where = "WHERE c.status = %s"
        parametros = (STATUS_CHAMADOS[indice_status],)

    elif opcao_filtro == 3:
        prioridades = ["Alta", "Media", "Baixa"]

        print()
        print("+----+------------+")
        print("| No | Prioridade |")
        print("+----+------------+")

        for i, prioridade in enumerate(prioridades):
            print(f"| {i + 1:<2} | {prioridade:<10} |")

        print("+----+------------+")

        indice_prioridade = ler_inteiro_entre(1, len(prioridades), "Selecione a prioridade: ") - 1
        where = "WHERE c.prioridade = %s"
        parametros = (prioridades[indice_prioridade],)

    conexao = obter_conexao()

    if conexao is None:
        print("Não foi possível ver os chamados: sem conexão com o banco.\n")
        return

    cursor = None

    try:
        cursor = conexao.cursor()
        consulta = f"""
            SELECT
                c.id_chamado,
                p.nome,
                m.nome,
                m.especialidade,
                c.descricao,
                c.urgencia,
                c.prioridade,
                c.status,
                DATE_FORMAT(c.data_abertura, '%d/%m/%Y %H:%i')
            FROM chamados c
            INNER JOIN pacientes p ON c.id_paciente = p.id_paciente
            INNER JOIN medicos m ON c.id_medico = m.id_medico
            {where}
            ORDER BY c.data_abertura DESC
            """
        cursor.execute(consulta, parametros)
        chamados = cursor.fetchall()

    except Exception as erro:
        print("Erro ao buscar chamados no banco de dados:")
        print(erro)
        print()
        return

    finally:
        if cursor:
            cursor.close()

        fechar_conexao(conexao)

    if not chamados:
        print("\nNenhum chamado cadastrado.\n")
        return

    print()
    print("+------+----------------------+----------------------+---------------+----------+------------+---------------+------------------+")
    print("| ID   | Paciente             | Medico               | Especialidade | Urgencia | Prioridade | Status        | Abertura         |")
    print("+------+----------------------+----------------------+---------------+----------+------------+---------------+------------------+")

    for chamado in chamados:
        id_chamado, paciente, medico, especialidade, descricao, urgencia, prioridade, status, data_abertura = chamado
        print(
            f"| {id_chamado:<4} | "
            f"{paciente[:20]:<20} | "
            f"{medico[:20]:<20} | "
            f"{especialidade[:13]:<13} | "
            f"{urgencia:<8} | "
            f"{prioridade[:10]:<10} | "
            f"{status[:13]:<13} | "
            f"{data_abertura:<16} |"
        )

    print("+------+----------------------+----------------------+---------------+----------+------------+---------------+------------------+")
    print("\nDescrições:")

    for chamado in chamados:
        id_chamado = chamado[0]
        descricao = chamado[4]
        print(f"{id_chamado} - {descricao}")

    print()


def alterar_status_chamado(novo_status):
    conexao = obter_conexao()

    if conexao is None:
        print("Não foi possível atualizar o status: sem conexão com o banco.\n")
        return

    cursor = None

    try:
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT
                c.id_chamado,
                p.nome,
                c.status
            FROM chamados c
            INNER JOIN pacientes p ON c.id_paciente = p.id_paciente
            ORDER BY c.data_abertura DESC
            """
        )
        chamados = cursor.fetchall()

        if not chamados:
            print("\nNenhum chamado cadastrado.\n")
            return

        print()
        print("+------+----------------------+---------------+")
        print("| ID   | Paciente             | Status        |")
        print("+------+----------------------+---------------+")

        for id_chamado, paciente, status in chamados:
            print(f"| {id_chamado:<4} | {paciente[:20]:<20} | {status[:13]:<13} |")

        print("+------+----------------------+---------------+")

        ids_chamados = [chamado[0] for chamado in chamados]

        while True:
            id_chamado = ler_inteiro_entre(1, 999999, "Digite o ID do chamado: ")

            if id_chamado in ids_chamados:
                break

            print("Não foi encontrado chamado com esse ID.\n")

        cursor.execute(
            """
            UPDATE chamados
            SET status = %s
            WHERE id_chamado = %s
            """,
            (novo_status, id_chamado)
        )
        conexao.commit()

    except Exception as erro:
        conexao.rollback()
        print("Erro ao atualizar status do chamado:")
        print(erro)
        print()
        return

    finally:
        if cursor:
            cursor.close()

        fechar_conexao(conexao)

    print(f"Status do chamado {id_chamado} atualizado para '{novo_status}'.\n")


def listar_medicos():
    conexao = obter_conexao()

    if conexao is None:
        return None

    cursor = None

    try:
        cursor = conexao.cursor()

        cursor.execute("SELECT id_medico, crm, nome, especialidade FROM medicos")
        medicos = cursor.fetchall()

        print("\n--- LISTA DE MÉDICOS ---")
        for id_medico, crm, nome, especialidade in medicos:
            print(f"ID: {id_medico} | CRM: {crm} | Nome: {nome} | Especialidade: {especialidade}")
        print("------------------------\n")

    except Exception as erro:
        print("Erro:", erro)
    
    finally:
        if cursor:
            cursor.close()
        fechar_conexao(conexao)

def iniciar_chamado():
    alterar_status_chamado("Em andamento")


def finalizar_chamado():
    alterar_status_chamado("Fechada")


def mostrar_menu():
    print("===== SISTEMA HOSPITALAR =====")
    print("1 - Adicionar paciente")
    print("2 - Chamar próximo paciente")
    print("3 - Ver fila")
    print("4 - Criar chamado")
    print("0 - Sair")
    print("==============================\n")
