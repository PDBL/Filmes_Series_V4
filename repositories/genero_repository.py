from database import obter_conexao


def obter_ou_criar_genero(nome):

    conexao = obter_conexao()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        "SELECT id FROM generos WHERE nome = %s",
        (nome,)
    )

    genero = cursor.fetchone()

    if genero:
        cursor.close()
        conexao.close()
        return genero["id"]

    cursor.execute(
        "INSERT INTO generos (nome) VALUES (%s)",
        (nome,)
    )

    genero_id = cursor.lastrowid

    conexao.commit()

    cursor.close()
    conexao.close()

    return genero_id


def associar_genero(serie_id, genero_id):

    conexao = obter_conexao()
    cursor = conexao.cursor()

    sql = """
        INSERT IGNORE INTO series_generos
        (serie_id, genero_id)
        VALUES (%s, %s)
    """

    cursor.execute(
        sql,
        (serie_id, genero_id)
    )

    conexao.commit()

    cursor.close()
    conexao.close()


def listar_generos():

    conexao = obter_conexao()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, nome FROM generos ORDER BY nome"
    )

    resultados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return resultados