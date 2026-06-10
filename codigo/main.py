# --------------------------------------------
# Sistema de fila hospitalar por prioridade
# Prioridade:
# 1º Média (maior primeiro)
# 2º Urgência (desempate)
# --------------------------------------------


# Importa módulos do sistema para manipulação de caminhos
import sys
import os


# Adiciona o diretório raiz do projeto ao caminho de importação do Python
# Isso permite importar arquivos da pasta "src" mesmo executando esse arquivo de outro local
# Explicando:
# __file__ → caminho do arquivo atual
# abspath → caminho absoluto
# dirname → sobe um nível na pasta
# dirname novamente → sobe mais um nível (até a raiz do projeto)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Importa funções do módulo fila_service
# Essas funções são responsáveis pela lógica do sistema (regras de negócio)

# Função que cadastra um novo paciente
from src.services.fila_service import adicionar_paciente

# Função que cadastra um novo médico
from src.services.fila_service import adicionar_medico

# Função que cria um chamado (liga paciente + médico + prioridade)
from src.services.fila_service import criar_chamado

# Função que finaliza um chamado (status → Fechada)
from src.services.fila_service import finalizar_chamado

# Função que inicia um chamado (status → Em andamento)
from src.services.fila_service import iniciar_chamado

# Função que lista todos os pacientes cadastrados no banco
from src.services.fila_service import listar_pacientes

# Função que mostra os chamados (com filtros)
from src.services.fila_service import ver_chamados

# Função que lista todos os médicos cadastrados
from src.services.fila_service import listar_medicos


# Função responsável apenas por EXIBIR o menu na tela
def mostrar_menu():
    print()

    # Desenha o menu com layout visual organizado
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


# Função principal do sistema (controla o fluxo do menu)
def menu():

    # Loop infinito: o sistema continua rodando até o usuário escolher sair
    while True:

        # Mostra o menu na tela
        mostrar_menu()

        # Captura a opção digitada pelo usuário
        opcao = input("Escolha: ")


        # Verifica qual opção o usuário escolheu e chama a função correspondente

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
            # Caso o usuário digite uma opção inválida
            print("\nOpcao invalida. Tente novamente.\n")


# Chama a função menu para iniciar o sistema
# Esse é o ponto de entrada do programa
menu()
