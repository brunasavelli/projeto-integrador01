import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.fila_service import adicionar_paciente
from src.services.fila_service import adicionar_medico
from src.services.fila_service import criar_chamado
from src.services.fila_service import finalizar_chamado
from src.services.fila_service import iniciar_chamado
from src.services.fila_service import listar_pacientes
from src.services.fila_service import ver_chamados
from src.services.fila_service import listar_medicos


def mostrar_menu():
    print()

    print("+--------------------------------------+")
    print("|        SISTEMA FILA HOSPITALAR       |")
    print("+--------------------------------------+")
    print("|  1  - Cadastrar paciente             |")
    print("|  2  - Abrir chamado                  |")
    print("|  3  - Ver chamados                   |")
    print("|  4  - Iniciar chamado                |")
    print("|  5  - Finalizar chamado              |")
    print("|  6  - Adicionar medico               |")
    print("|  7  - Listar pacientes               |")
    print("|  8  - Listar medicos                 |")
    print("|  0  - Sair                           |")
    print("+--------------------------------------+")


def menu():

    while True:

        # Mostra o menu na tela
        mostrar_menu()

        # Captura a opção digitada pelo usuário
        opcao = input("Escolha: ")


        if opcao == "1":
            # Chama função para cadastrar paciente
            adicionar_paciente()

        elif opcao == "2":
            # Chama função para criar chamado
            criar_chamado()

        elif opcao == "3":
            # Mostra todos os chamados
            ver_chamados()

        elif opcao == "4":
            # Inicia atendimento de um chamado (muda status)
            iniciar_chamado()

        elif opcao == "5":
            # Finaliza atendimento de um chamado
            finalizar_chamado()

        elif opcao == "6":
            # Cadastra um novo médico
            adicionar_medico()

        elif opcao == "7":
            # Lista pacientes cadastrados
            listar_pacientes()

        elif opcao == "8":
            # Lista médicos cadastrados
            listar_medicos()

        elif opcao == "0":
            # Encerra o sistema
            print("\nEncerrando sistema...\n")
            break

        else:
            print("\nOpcao invalida. Tente novamente.\n")


menu()
