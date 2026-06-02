# --------------------------------------------
# Sistema de fila hospitalar por prioridade
# Prioridade:
# 1º Média (maior primeiro)
# 2º Urgência (desempate)
# --------------------------------------------

from src.services.fila_service import (
    adicionar_paciente,
    listar_pacientes,
    adicionar_medico,
    listar_medicos,
    ver_chamados,
    criar_chamado,
    iniciar_chamado,
    finalizar_chamado,

    status_em_espera,
    status_em_andamento,
    status_finalizado,
    prioridade_alta,
    prioridade_media,
    prioridade_baixa
)

def mostrar_menu():
    print("+----------------------------------------+")
    print("|          SISTEMA HOSPITALAR            |")
    print("+----------------------------------------+")
    print("|   1 - Adicionar paciente               |")
    print("|   2 - Listar pacientes                 |")
    print("|   3 - Adicionar médico                 |")
    print("|   4 - Listar médicos                   |")
    print("|   5 - Criar chamado                    |")
    print("|   6 - Ver chamados                     |")
    print("|   7 - Iniciar chamado                  |")
    print("|   8 - Finalizar chamado                |")
    print("|   0 - Sair                             |")
    print("+----------------------------------------+")


def submenu_chamados():
    while True:
        print("\n+-------------------------------------+")
        print("|         FILTRO DE CHAMADOS            |")
        print("+---------------------------------------+")
        print("| 1 - Ver chamados em espera            |")
        print("| 2 - Ver chamados em andamento         |")
        print("| 3 - Ver chamados finalizados          |")
        print("| 4 - Ver chamados com prioridade ALTA  |")
        print("| 5 - Ver chamados com prioridade MÉDIA |")
        print("| 6 - Ver chamados com prioridade BAIXA |")
        print("| 7 - Ver todos os chamados             |")
        print("| 0 - Voltar                            |")
        print("+---------------------------------------+")

        opcao = input("Escolha: ")

        if opcao == "1":
            chamados = status_em_espera()

            print("\n--- CHAMADOS EM ESPERA ---")
            for chamado in chamados:
                print(chamado)

        elif opcao == "2":
            chamados = status_em_andamento()

            print("\n--- CHAMADOS EM ANDAMENTO ---")
            for chamado in chamados:
                print(chamado)

        elif opcao == "3":
            chamados = status_finalizado()

            print("\n--- CHAMADOS FINALIZADOS ---")
            for chamado in chamados:
                print(chamado)

        elif opcao == "4":
            chamados = prioridade_alta()

            print("\n--- CHAMADOS COM PRIORIDADE ALTA ---")
            for chamado in chamados:
                print(chamado)

        elif opcao == "5":
            chamados = prioridade_media()

            print("\n--- CHAMADOS COM PRIORIDADE MÉDIA ---")
            for chamado in chamados:
                print(chamado)

        elif opcao == "6":
            chamados = prioridade_baixa()

            print("\n--- CHAMADOS COM PRIORIDADE BAIXA ---")
            for chamado in chamados:
                print(chamado)

        elif opcao == "7":
            ver_chamados()

        elif opcao == "0":
            break

        else:
            print("Opção inválida!")

def menu():
    while True:
        mostrar_menu()
        opcao = input("Escolha: ")

        if opcao == "1":
            adicionar_paciente()

        elif opcao == "2":
            listar_pacientes()

        elif opcao == "3":
            adicionar_medico()
        
        elif opcao == "4":
            listar_medicos()

        elif opcao == "5":
            criar_chamado()
        
        elif opcao == "6":
            submenu_chamados()

        elif opcao == "7":
            iniciar_chamado()

        elif opcao == "8":
            finalizar_chamado()

        elif opcao == "0":
            break


menu()