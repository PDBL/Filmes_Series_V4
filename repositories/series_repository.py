from database import obter_conexao


def procurar_por_tvmaze_id(tvmaze_id: int):

    conexao = obter_conexao()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM series WHERE tvmaze_id = %s",
        (tvmaze_id,)
    )

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado


def inserir_serie(dados):

    conexao = obter_conexao()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO series (
            tvmaze_id,
            nome,
            tipo,
            idioma,
            estado,
            data_estreia,
            data_fim,
            duracao,
            classificacao,
            canal,
            resumo,
            imagem
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    valores = (
        dados["tvmaze_id"],
        dados["nome"],
        dados["tipo"],
        dados["idioma"],
        dados["estado"],
        dados["data_estreia"],
        dados["data_fim"],
        dados["duracao"],
        dados["classificacao"],
        dados["canal"],
        dados["resumo"],
        dados["imagem"]
    )

    cursor.execute(sql, valores)

    serie_id = cursor.lastrowid

    conexao.commit()

    cursor.close()
    conexao.close()

    return serie_id


def listar_series(nome=None, genero=None):

    conexao = obter_conexao()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT DISTINCT
            s.id,
            s.tvmaze_id,
            s.nome,
            s.tipo,
            s.idioma,
            s.estado,
            s.data_estreia,
            s.data_fim,
            s.duracao,
            s.classificacao,
            s.canal,
            s.resumo,
            s.imagem
        FROM series s
        LEFT JOIN series_generos sg
            ON s.id = sg.serie_id
        LEFT JOIN generos g
            ON sg.genero_id = g.id
        WHERE 1=1
    """

    parametros = []

    if nome:
        sql += " AND s.nome LIKE %s"
        parametros.append(f"%{nome}%")

    if genero:
        sql += " AND g.nome = %s"
        parametros.append(genero)

    sql += " ORDER BY s.nome"

    cursor.execute(sql, parametros)

    resultados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return resultados


def procurar_serie_id(id_serie):

    conexao = obter_conexao()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT
            id,
            tvmaze_id,
            nome,
            tipo,
            idioma,
            estado,
            data_estreia,
            data_fim,
            duracao,
            classificacao,
            canal,
            resumo,
            imagem
        FROM series
        WHERE id = %s
    """

    cursor.execute(sql, (id_serie,))

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado