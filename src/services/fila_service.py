from src.data.fila import fila
from src.config.database import fechar_conexao, obter_conexao
from src.utils.input_utils import ler_inteiro_entre

# FUNÇÕES AUXILIARES

def calcular_media(impacto, urgencia):
    return (impacto + urgencia) / 2

def definir_prioridade(media):
    if media >= 4:
        return 'Alta'

    if media >= 2.5:
        return 'Media'

    return 'Baixa'


# FUNÇÕES DE PACIENTES
def adicionar_paciente():
    conexao = obter_conexao()

    if conexao is None:
        return None

    cursor = None

    try:
        cursor = conexao.cursor()

        sql = """
        INSERT INTO pacientes (nome, data_nascimento, telefone, email)
        VALUES (%s, %s, %s, %s)
        """
        nome = input("Digite o nome do paciente: ")
        data_nascimento = input("Digite a data de nascimento (YYYY-MM-DD): ")
        telefone = input("Digite o telefone: ")
        email = input("Digite o email: ")
        valores = (nome, data_nascimento, telefone, email)
        cursor.execute(sql, valores)

        conexao.commit()

        return cursor.lastrowid  

    except Exception as erro:
        print("Erro:", erro)
        return None
    
    finally:
        if cursor:
            cursor.close()
        fechar_conexao(conexao)

def listar_pacientes():
    conexao = obter_conexao()

    if conexao is None:
        return None

    cursor = None

    try:
        cursor = conexao.cursor()

        cursor.execute("SELECT id_paciente, nome, data_nascimento, telefone, email FROM pacientes")
        pacientes = cursor.fetchall()

        print("\n--- LISTA DE PACIENTES ---")
        for id_paciente, nome, data_nascimento, telefone, email in pacientes:
            print(f"ID: {id_paciente} | Nome: {nome} | Data de Nascimento: {data_nascimento} | Telefone: {telefone} | Email: {email}")
        print("--------------------------\n")

    except Exception as erro:
        print("Erro:", erro)
    
    finally:
        if cursor:
            cursor.close()
        fechar_conexao(conexao)

# FUNÇÕES DE MÉDICOS

def adicionar_medico():
    conexao = obter_conexao()

    if conexao is None:
        return None

    cursor = None

    try:
        cursor = conexao.cursor()

        sql = """
            INSERT INTO medicos (crm, nome, especialidade)
            VALUES (%s, %s, %s)
        """

        crm = input("Digite o CRM do médico: ")
        nome = input("Digite o nome do médico: ")
        especialidade = input("Digite a especialidade: ")

        valores = (crm, nome, especialidade)

        cursor.execute(sql, valores)
        conexao.commit()

        print("Médico inserido com sucesso!")

    except Exception as erro:
        print("Erro:", erro)
        conexao.rollback()
    finally:
        if cursor:
            cursor.close()

        fechar_conexao(conexao)

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

# FUNÇÕES DE CHAMADOS

def criar_chamado():
    conexao = obter_conexao()

    if conexao is None:
        print("Não foi possível conectar ao banco.\n")
        return

    cursor = None

    try:
        cursor = conexao.cursor()

        # Buscar pacientes cadastrados
        cursor.execute("""
            SELECT id_paciente, nome
            FROM pacientes
            ORDER BY nome
        """)

        pacientes = cursor.fetchall()

        if not pacientes:
            print("Não há pacientes cadastrados.\n")
            return

        print("\n--- PACIENTES CADASTRADOS ---")
        for i, (id_paciente, nome) in enumerate(pacientes, start=1):
            print(f"{i} - {nome} (ID: {id_paciente})")
        print("-----------------------------\n")

        indice = ler_inteiro_entre(
            1,
            len(pacientes),
            "Selecione o paciente: "
        ) - 1

        id_paciente, nome = pacientes[indice]

        descricao = input("Descrição do chamado: ").strip()

        if not descricao:
            print("Descrição não pode ser vazia.\n")
            return

        urgencia = ler_inteiro_entre(
            1,
            5,
            "Informe a urgência (1 a 5): "
        )

        impacto = ler_inteiro_entre(
            1,
            5,
            "Informe o impacto (1 a 5): "
        )

        media = calcular_media(impacto, urgencia)
        prioridade = definir_prioridade(media)

        cursor.execute("""
            SELECT id_medico, crm, nome, especialidade
            FROM medicos
            ORDER BY nome
        """)

        medicos = cursor.fetchall()

        if not medicos:
            print("Não há médicos cadastrados.\n")
            return

        print("\n--- MÉDICOS CADASTRADOS ---")

        for i, (id_medico, crm, nome_medico, especialidade) in enumerate(
            medicos,
            start=1
        ):
            print(
                f"{i} - {nome_medico} | "
                f"CRM: {crm} | "
                f"Especialidade: {especialidade}"
            )

        print("---------------------------\n")

        indice_medico = ler_inteiro_entre(
            1,
            len(medicos),
            "Selecione o médico: "
        ) - 1

        id_medico = medicos[indice_medico][0]

        cursor.execute(
            """
            INSERT INTO chamados (
                id_paciente,
                id_medico,
                descricao,
                urgencia,
                impacto,
                prioridade
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                id_paciente,
                id_medico,
                descricao,
                urgencia,
                impacto,
                prioridade
            )
        )

        conexao.commit()

        print(
            f"\nChamado criado com sucesso para "
            f"'{nome}' com prioridade {prioridade}.\n"
        )

    except Exception as erro:
        conexao.rollback()
        print("Erro ao criar chamado:")
        print(erro)

    finally:
        if cursor:
            cursor.close()

        fechar_conexao(conexao)

def ver_chamados():
    conexao = obter_conexao()

    if conexao is None:
        print("Não foi possível consultar chamados: sem conexão com o banco.\n")
        return

    cursor = None

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT c.id_chamado, p.nome, m.nome, m.crm, c.descricao, c.urgencia, c.impacto, c.prioridade, c.status, c.data_abertura
            FROM chamados c
            JOIN pacientes p ON c.id_paciente = p.id_paciente
            JOIN medicos m ON c.id_medico = m.id_medico
            ORDER BY c.data_abertura DESC
        """)

        chamados = cursor.fetchall()

        if not chamados:
            print("Nenhum chamado encontrado.\n")
            return

        print("\n--- LISTA DE CHAMADOS ---")
        for (
            id_chamado,
            nome_paciente,
            nome_medico,
            crm,
            descricao,
            urgencia,
            impacto,
            prioridade,
            status,
            data_abertura
        ) in chamados:

            print(
                f"ID: {id_chamado} | "
                f"Paciente: {nome_paciente} | "
                f"Médico: {nome_medico} | "
                f"CRM: {crm} | "
                f"Descrição: {descricao} | "
                f"Urgência: {urgencia} | "
                f"Impacto: {impacto} | "
                f"Prioridade: {prioridade} | "
                f"Status: {status}"
            )

    except Exception as erro:
        print("Erro ao consultar chamados no banco de dados:")
        print(erro)
        print()
    
    finally:
        if cursor:
            cursor.close()
        fechar_conexao(conexao)

def iniciar_chamado():
    conexao = obter_conexao()

    if conexao is None:
        print("Não foi possível iniciar chamado: sem conexão com o banco.\n")
        return

    cursor = None

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                c.id_chamado,
                p.nome,
                c.descricao,
                c.prioridade
            FROM chamados c
            JOIN pacientes p
                ON c.id_paciente = p.id_paciente
            WHERE c.status = 'Em Espera'
            ORDER BY c.data_abertura
        """)

        chamados = cursor.fetchall()

        if not chamados:
            print("Não há chamados em espera.\n")
            return

        print("\n--- CHAMADOS EM ESPERA ---")

        for i, (
            id_chamado,
            nome_paciente,
            descricao,
            prioridade
        ) in enumerate(chamados, start=1):

            print(
                f"{i} - "
                f"Paciente: {nome_paciente} | "
                f"Descrição: {descricao} | "
                f"Prioridade: {prioridade}"
            )

        print("--------------------------\n")

        indice = ler_inteiro_entre(
            1,
            len(chamados),
            "Selecione o chamado: "
        ) - 1

        id_chamado = chamados[indice][0]

        cursor.execute(
            """
            UPDATE chamados
            SET status = 'Em Andamento'
            WHERE id_chamado = %s
            """,
            (id_chamado,)
        )

        conexao.commit()

        print(
            f"Chamado {id_chamado} iniciado com sucesso.\n"
        )

    except Exception as erro:
        conexao.rollback()
        print("Erro ao iniciar chamado:")
        print(erro)

    finally:
        if cursor:
            cursor.close()

        fechar_conexao(conexao)

def finalizar_chamado():
    conexao = obter_conexao()

    if conexao is None:
        print("Não foi possível finalizar chamado: sem conexão com o banco.\n")
        return

    cursor = None

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                c.id_chamado,
                p.nome,
                c.descricao,
                c.prioridade
            FROM chamados c
            JOIN pacientes p
                ON c.id_paciente = p.id_paciente
            WHERE c.status = 'Em Andamento'
            ORDER BY c.data_abertura
        """)

        chamados = cursor.fetchall()

        if not chamados:
            print("Não há chamados em andamento.\n")
            return

        print("\n--- CHAMADOS EM ANDAMENTO ---")

        for i, (
            id_chamado,
            nome_paciente,
            descricao,
            prioridade
        ) in enumerate(chamados, start=1):

            print(
                f"{i} - "
                f"Paciente: {nome_paciente} | "
                f"Descrição: {descricao} | "
                f"Prioridade: {prioridade}"
            )

        print("-----------------------------\n")

        indice = ler_inteiro_entre(
            1,
            len(chamados),
            "Selecione o chamado: "
        ) - 1

        id_chamado = chamados[indice][0]

        cursor.execute(
            """
            UPDATE chamados
            SET status = 'Finalizado'
            WHERE id_chamado = %s
            """,
            (id_chamado,)
        )

        conexao.commit()

        print(
            f"Chamado {id_chamado} finalizado com sucesso.\n"
        )

    except Exception as erro:
        conexao.rollback()
        print("Erro ao finalizar chamado:")
        print(erro)

    finally:
        if cursor:
            cursor.close()

        fechar_conexao(conexao)
    
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


# FILTROS DE STATUS

def status_em_espera():
    conexao = obter_conexao()

    if conexao is None:
        return []

    cursor = None

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id_chamado, id_paciente, id_medico, descricao, urgencia, impacto, prioridade, status, data_abertura
            FROM chamados
            WHERE status = 'Em Espera'
        """)

        return cursor.fetchall()

    except Exception as erro:
        print("Erro ao consultar chamados em espera:")
        print(erro)
        return []

    finally:
        if cursor:
            cursor.close()
        fechar_conexao(conexao)

def status_em_andamento():
    conexao = obter_conexao()

    if conexao is None:
        return []

    cursor = None

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id_chamado, id_paciente, id_medico, descricao, urgencia, impacto, prioridade, status, data_abertura
            FROM chamados
            WHERE status = 'Em Andamento'
        """)

        return cursor.fetchall()

    except Exception as erro:
        print("Erro ao consultar chamados em andamento:")
        print(erro)
        return []

    finally:
        if cursor:
            cursor.close()
        fechar_conexao(conexao)

def status_finalizado():
    conexao = obter_conexao()

    if conexao is None:
        return []

    cursor = None

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id_chamado, id_paciente, id_medico, descricao, urgencia, impacto, prioridade, status, data_abertura
            FROM chamados
            WHERE status = 'Finalizado'
        """)

        return cursor.fetchall()

    except Exception as erro:
        print("Erro ao consultar chamados finalizados:")
        print(erro)
        return []

    finally:
        if cursor:
            cursor.close()
        fechar_conexao(conexao)


# FILTROS DE PRIORIDADE

def prioridade_alta():
    conexao = obter_conexao()

    if conexao is None:
        return []

    cursor = None

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id_chamado, id_paciente, id_medico, descricao, urgencia, impacto, prioridade, status, data_abertura
            FROM chamados
            WHERE prioridade = 'Alta'
        """)

        return cursor.fetchall()

    except Exception as erro:
        print("Erro ao consultar chamados com prioridade ALTA:")
        print(erro)
        return []

    finally:
        if cursor:
            cursor.close()
        fechar_conexao(conexao)

def prioridade_media():
    conexao = obter_conexao()

    if conexao is None:
        return []

    cursor = None

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id_chamado, id_paciente, id_medico, descricao, urgencia, impacto, prioridade, status, data_abertura
            FROM chamados
            WHERE prioridade = 'Media'
        """)

        return cursor.fetchall()

    except Exception as erro:
        print("Erro ao consultar chamados com prioridade MÉDIA:")
        print(erro)
        return []

    finally:
        if cursor:
            cursor.close()
        fechar_conexao(conexao)

def prioridade_baixa():
    conexao = obter_conexao()

    if conexao is None:
        return []

    cursor = None

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id_chamado, id_paciente, id_medico, descricao, urgencia, impacto, prioridade, status, data_abertura
            FROM chamados
            WHERE prioridade = 'Baixa'
        """)

        return cursor.fetchall()

    except Exception as erro:
        print("Erro ao consultar chamados com prioridade BAIXA:")
        print(erro)
        return []

    finally:
        if cursor:
            cursor.close()
        fechar_conexao(conexao)
