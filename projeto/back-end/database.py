import mysql.connector

def conectar():
    conexao = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="963968",
        database="loja_boosting"
    )

    return conexao
