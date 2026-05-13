# --------------------------------------------
# Sistema de fila hospitalar por prioridade
# Prioridade:
# 1º Média (maior primeiro)
# 2º Urgência (desempate)
# --------------------------------------------

from src.services.fila_service import adicionar_paciente
from src.services.chamados_service import abrir_chamado

def menu():
    while True:
        print("\n1 - Cadastrar paciente")
        print("2 - Abrir chamado")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            adicionar_paciente()

        elif opcao == "2":
            abrir_chamado()

        elif opcao == "0":
            break

menu()