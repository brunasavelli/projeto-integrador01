# Função que lê um número inteiro digitado pelo usuário,
# garantindo que ele esteja dentro de um intervalo válido (entre min_val e max_val)
def ler_inteiro_entre(min_val=1, max_val=5, prompt="Digite um número: "):
    
    # Loop infinito: vai continuar pedindo o valor até o usuário digitar corretamente
    while True:
        
        # Mostra a mensagem (prompt) e captura o que o usuário digitou
        # Exemplo: "Digite um número: "
        val = input(prompt)

        # Verifica se o valor digitado contém apenas números (sem letras ou símbolos)
        # isdigit() retorna True se for um número inteiro positivo (ex: "123")
        if not val.isdigit():
            
            # Se NÃO for número, mostra mensagem de erro
            print(f"Informe um número inteiro entre {min_val} e {max_val}.")
            
            # 'continue' faz o loop voltar para o início (pede o número de novo)
            continue

        # Converte o valor digitado (string) para inteiro
        # Exemplo: "3" → 3
        num = int(val)

        # Verifica se o número está fora do intervalo permitido
        # (menor que o mínimo ou maior que o máximo)
        if num < min_val or num > max_val:
            
            # Se estiver fora do intervalo, mostra mensagem de erro
            print(f"Informe um número entre {min_val} e {max_val}.")
            
            # Volta para o início do loop para pedir novamente
            continue

        # Se chegou aqui:
        # ✔ é número
        # ✔ está dentro do intervalo
        # então retorna o valor e encerra a função
        return num
