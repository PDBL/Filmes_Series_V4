import mysql.connector


def obter_conexao():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        database="filmes_series"
    )