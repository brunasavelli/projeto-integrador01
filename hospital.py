# --------------------------------------------
# Sistema de fila hospitalar por prioridade
# Prioridade:
# 1º Urgência (maior primeiro)
# 2º Impacto (desempate)
# --------------------------------------------

import heapq

fila = []

def ler_inteiro_entre(min_val=1, max_val=5, prompt="Digite um número: "):
    while True:
        val = input(prompt).strip()
        if not val.isdigit():
            print(f"Informe um número inteiro entre {min_val} e {max_val}.")
            continue
        num = int(val)
        if num < min_val or num > max_val:
            print(f"Informe um número entre {min_val} e {max_val}.")
            continue
        return num

def calcular_media(impacto: int, urgencia: int) -> float:
    return (impacto + urgencia) / 2.0

def adicionar_paciente():
    nome = input("Nome do paciente: ").strip()
    if not nome:
        print("Nome não pode ser vazio.\n")
        return

    impacto = ler_inteiro_entre(1, 5, "Impacto (1 a 5): ")
    urgencia = ler_inteiro_entre(1, 5, "Urgência (1 a 5): ")

    media = calcular_media(impacto, urgencia)

    # heapq é min-heap → usamos valores negativos para priorizar maiores
    heapq.heappush(fila, (-urgencia, -impacto, nome, impacto, urgencia, media))

    print(f"✅ Paciente '{nome}' adicionado com urgência {urgencia} e impacto {impacto}.\n")

def chamar_proximo():
    if not fila:
        print("ℹ️  Não há pacientes na fila.\n")
        return

    _, _, nome, impacto, urgencia, media = heapq.heappop(fila)

    print("\nChamando próximo paciente:\n")
    print(f"   Nome: {nome}")
    print(f"   Impacto: {impacto}")
    print(f"   Urgência: {urgencia}")
    print(f"   Média: {media:.1f}\n")

def ver_fila():
    if not fila:
        print("Fila vazia.\n")
        return

    print("\n--- FILA ATUAL (ordenada por prioridade) ---")

    # heap não é ordenado visualmente → precisamos ordenar para exibir
    fila_ordenada = sorted(fila)

    for item in fila_ordenada:
        urg_neg, imp_neg, nome, impacto, urgencia, media = item
        print(f"{nome} | Urgência: {urgencia} | Impacto: {impacto} | Média: {media:.1f}")

    print("------------------------------------------\n")

def mostrar_menu():
    print("===== SISTEMA HOSPITALAR =====")
    print("1 - Adicionar paciente")
    print("2 - Chamar próximo paciente")
    print("3 - Ver fila")
    print("0 - Sair")
    print("==============================\n")

# --------- Loop principal ---------
if __name__ == "__main__":
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            adicionar_paciente()
        elif opcao == "2":
            chamar_proximo()
        elif opcao == "3":
            ver_fila()
        elif opcao == "0":
            print("Encerrando o sistema. Até breve!")
            break
        else:
            print("Opção inválida.\n")