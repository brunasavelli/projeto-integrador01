from src.data.fila import fila
from src.utils.input_utils import ler_inteiro_entre

def calcular_media(impacto, urgencia):
    return (impacto + urgencia) / 2


def adicionar_paciente():
    nome = input("Nome do paciente: ")

    if nome == "":
        print("Nome não pode ser vazio.\n")
        return

    impacto = ler_inteiro_entre(1, 5, "Impacto (1 a 5): ")
    urgencia = ler_inteiro_entre(1, 5, "Urgência (1 a 5): ")

    media = calcular_media(impacto, urgencia)

    fila.append([nome, impacto, urgencia, media])

    print(f"✅ Paciente '{nome}' adicionado.\n")



def criar_chamado():
    if not fila:
        print("Não há pacientes na fila para criar um chamado.\n")
        return

    print("\n--- PACIENTES NA FILA ---")
    for i, (nome, impacto, urgencia, media, *_) in enumerate(fila):
        print(f"{i + 1} - {nome} | Urgência: {urgencia} | Impacto: {impacto} | Média: {media:.1f}")
    print("-------------------------\n")

    indice = ler_inteiro_entre(1, len(fila), "Selecione o número do paciente: ") - 1

    descricao = input("Descrição do chamado: ").strip()

    if descricao == "":
        print("Descrição não pode ser vazia.\n")
        return

    if len(fila[indice]) == 4:
        fila[indice].append([])  # inicializa lista de chamados se ainda não existir

    fila[indice][4].append(descricao)

    print(f"Chamado criado para '{fila[indice][0]}'.\n")



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

    for paciente in fila:
        nome, impacto, urgencia, media = paciente[:4]
        chamados = paciente[4] if len(paciente) > 4 else []
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
    print("4 - Criar chamado")
    print("0 - Sair")
    print("==============================\n")