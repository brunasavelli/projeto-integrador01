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


def listar_medicos(cursor):
    cursor.execute(
        """
        SELECT id_medico, nome, especialidade
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
    nome = input("Nome do paciente: ").strip()

    if nome == "":
        print("Nome não pode ser vazio.\n")
        return

    data_nascimento = input("Data de nascimento (AAAA-MM-DD): ").strip()

    if data_nascimento == "":
        print("Data de nascimento nao pode ser vazia.\n")
        return

    telefone = input("Telefone do paciente: ").strip()

    if telefone == "":
        print("Telefone nao pode ser vazio.\n")
        return

    email = input("Email do paciente: ").strip()

    if email == "":
        print("Email nao pode ser vazio.\n")
        return

    impacto = ler_inteiro_entre(1, 5, "Impacto (1 a 5): ")
    urgencia = ler_inteiro_entre(1, 5, "Urgência (1 a 5): ")

    media = calcular_media(impacto, urgencia)

    fila.append([nome, impacto, urgencia, media, data_nascimento, telefone, email])

    print(f" Paciente '{nome}' adicionado.\n")


def adicionar_medico():
    nome = input("Nome do medico: ").strip()

    if nome == "":
        print("Nome nao pode ser vazio.\n")
        return
    

    especialidade = input("Especialidade: ").strip()

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
            """
            INSERT INTO medicos (nome, especialidade)
            VALUES (%s, %s)
            """,
            (nome, especialidade)
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
    for i, (nome, impacto, urgencia, media, *_) in enumerate(fila):
        print(f"{i + 1} - {nome} | Urgência: {urgencia} | Impacto: {impacto} | Média: {media:.1f}")
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

    nome, impacto, urgencia, media, data_nascimento, telefone, email = fila[indice][:7]
    prioridade = definir_prioridade(media)
    conexao = obter_conexao()

    if conexao is None:
        print("Não foi possível criar o chamado: sem conexão com o banco.\n")
        return

    cursor = None

    try:
        cursor = conexao.cursor()
        medicos = listar_medicos(cursor)

        if not medicos:
            print("Nenhum medico cadastrado. Cadastre um medico primeiro.\n")
            return

        while True:
            print()
            print("+----+---------------------+---------------+")
            print("| No | Medico              | Especialidade |")
            print("+----+---------------------+---------------+")
            for i, (_, nome_medico, especialidade) in enumerate(medicos):
                print(f"| {i + 1:<2} | {nome_medico:<19} | {especialidade:<13} |")
            print("+----+---------------------+---------------+")

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

    if len(fila[indice]) == 7:
        fila[indice].append([])

    fila[indice][7].append(descricao)

    print(f"Chamado criado para '{nome}' com prioridade {prioridade}.\n")


def chamar_proximo():
    if not fila:
        print("Não há pacientes na fila.\n")
        return

    indice_maior = 0

    for i in range(1, len(fila)):

        if fila[i][3] > fila[indice_maior][3]:
            indice_maior = i

        elif fila[i][3] == fila[indice_maior][3]:

            if fila[i][2] > fila[indice_maior][2]:
                indice_maior = i

    paciente = fila.pop(indice_maior)

    nome, impacto, urgencia, media = paciente[:4]

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

    for paciente in fila:
        nome, impacto, urgencia, media = paciente[:4]
        print(
            f"{nome} | "
            f"Urgência: {urgencia} | "
            f"Impacto: {impacto} | "
            f"Média: {media:.1f}"
        )

    print("------------------\n")


def ver_chamados():
    conexao = obter_conexao()

    if conexao is None:
        print("Não foi possível ver os chamados: sem conexão com o banco.\n")
        return

    cursor = None

    try:
        cursor = conexao.cursor()
        cursor.execute(
            """
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
            ORDER BY c.data_abertura DESC
            """
        )
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


def atualizar_status_chamado():
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

        print()
        print("+----+---------------+")
        print("| No | Novo status   |")
        print("+----+---------------+")

        for i, status in enumerate(STATUS_CHAMADOS):
            print(f"| {i + 1:<2} | {status:<13} |")

        print("+----+---------------+")

        indice_status = ler_inteiro_entre(1, len(STATUS_CHAMADOS), "Selecione o status: ") - 1
        novo_status = STATUS_CHAMADOS[indice_status]

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


def mostrar_menu():
    print("===== SISTEMA HOSPITALAR =====")
    print("1 - Adicionar paciente")
    print("2 - Chamar próximo paciente")
    print("3 - Ver fila")
    print("4 - Criar chamado")
    print("0 - Sair")
    print("==============================\n")
