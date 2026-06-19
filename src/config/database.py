import mysql.connector

from dotenv import load_dotenv

import os

load_dotenv(override=True)

def obter_conexao():

    try:
        
        conexao = mysql.connector.connect(

            host=os.getenv("HOST"),

            user=os.getenv("USER"),

            password=os.getenv("PASSWORD"),

            database=os.getenv("NAME")
        )

        return conexao

    except Exception as erro:

        print("Erro ao conectar:")
        print(erro)

        return None


def fechar_conexao(conexao):

    try:

        if conexao:

            conexao.close()

    except Exception as erro:

        print("Erro ao fechar conexão:")
        print(erro)

