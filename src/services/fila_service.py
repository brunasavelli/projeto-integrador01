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