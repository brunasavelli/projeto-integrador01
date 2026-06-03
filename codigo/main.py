# --------------------------------------------
# Sistema de fila hospitalar por prioridade
# Prioridade:
# 1º Média (maior primeiro)
# 2º Urgência (desempate)
# --------------------------------------------

from src.services.fila_service import adicionar_paciente
from src.services.fila_service import adicionar_medico
from src.services.fila_service import atualizar_status_chamado
from src.services.fila_service import criar_chamado
from src.services.fila_service import ver_chamados


def mostrar_menu():
    print()
    print("+--------------------------------------+")
    print("|        SISTEMA FILA HOSPITALAR       |")
    print("+--------------------------------------+")
    print("|  1  - Cadastrar paciente             |")
    print("|  2  - Abrir chamado                  |")
    print("|  3  - Ver chamados                   |")
    print("|  4  - Atualizar status               |")
    print("|  5  - Adicionar medico               |")
    print("|  0  - Sair                           |")
    print("+--------------------------------------+")


def menu():
    while True:
        mostrar_menu()

        opcao = input("Escolha: ")

        if opcao == "1":
            adicionar_paciente()

        elif opcao == "2":
            criar_chamado()

        elif opcao == "3":
            ver_chamados()

        elif opcao == "4":
            atualizar_status_chamado()

        elif opcao == "5":
            adicionar_medico()

        elif opcao == "0":
            print("\nEncerrando sistema...\n")
            break

        else:
            print("\nOpcao invalida. Tente novamente.\n")


menu()
