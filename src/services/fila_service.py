def adicionar_paciente():
    #tenta abrir a conexão com o banco de dados
    conexao = obter_conexao()

    #se não conseguir conectar para a função
    if conexao is None:
        return None

    try:
        #cria um "cursor" que é o objeto usado para executar comandos sql
        cursor = conexao.cursor()

        #comando sql para inserir o paciente da tabela
        sql = """
        INSERT INTO pacientes (nome, data_nascimento, telefone, email)
        VALUES ('raquel', '2008-03-05', '(19)98855-2293', 'raquel@gmail.com')
        """

        #executa o comando sql no banco
        cursor.execute(sql)

        #salva (confirma) a altração no banco
        conexao.commit()

        #retorna o ID do ultimo registro inserido 
        return cursor.lastrowid  

    except Exception as erro:
        #se encontrar algum erro, mostra na tela
        print("Erro:", erro)

        #fecha o cursor
        cursor.close()

        #fecha a conexao com o banco
        fechar_conexao(conexao)

        #retorna none indicando que deu erro
        return None
