# --------------------------------------------
# Sistema de fila hospitalar por prioridade
# Prioridade:
# 1º Média (maior primeiro)
# 2º Urgência (desempate)
# --------------------------------------------

fila = []

def ler_inteiro_entre(min_val=1, max_val=5, prompt="Digite um número: "):
    while True:
        val = input(prompt)
        
        if not val.isdigit():
            print(f"Informe um número inteiro entre {min_val} e {max_val}.")
            continue
        
        num = int(val)
        
        if num < min_val or num > max_val:
            print(f"Informe um número entre {min_val} e {max_val}.")
            continue
        
        return num

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
        print("ℹ️  Não há pacientes na fila.\n")
        return

    # Encontrar o índice do paciente com maior prioridade
    indice_maior = 0

    for i in range(1, len(fila)):
        # compara média primeiro
        if fila[i][3] > fila[indice_maior][3]:
            indice_maior = i
        # desempate por urgência
        elif fila[i][3] == fila[indice_maior][3]:
            if fila[i][2] > fila[indice_maior][2]:
                indice_maior = i

    paciente = fila.pop(indice_maior)
    nome, impacto, urgencia, media = paciente

    print("\nChamando próximo paciente:\n")
    print(f"   Nome: {nome}")
    print(f"   Impacto: {impacto}")
    print(f"   Urgência: {urgencia}")
    print(f"   Média: {media:.1f}\n")

def ver_fila():
    if not fila:
        print("Fila vazia.\n")
        return

    print("\n--- FILA ATUAL ---")

    for nome, impacto, urgencia, media in fila:
        print(f"{nome} | Urgência: {urgencia} | Impacto: {impacto} | Média: {media:.1f}")

    print("------------------\n")

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
        opcao = input("Escolha uma opção: ")

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
