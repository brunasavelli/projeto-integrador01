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