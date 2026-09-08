from services.tvmaze_service import obter_serie_tvmaze
from repositories.series_repository import (
    procurar_por_tvmaze_id,
    inserir_serie
)
from repositories.genero_repository import (
    obter_ou_criar_genero,
    associar_genero
)


SERIES_INICIAIS = [
    "Breaking Bad",
    "Game of Thrones",
    "Stranger Things",
    "The Office",
    "Friends",
    "Sherlock",
    "The Walking Dead",
    "House",
    "The Last of Us",
    "Dark"
]


async def importar_series():

    resultados = []

    for nome in SERIES_INICIAIS:

        dados = await obter_serie_tvmaze(nome)

        if dados is None:
            resultados.append({
                "nome": nome,
                "estado": "não encontrada"
            })
            continue

        tvmaze_id = dados["id"]

        existente = procurar_por_tvmaze_id(tvmaze_id)

        if existente:
            resultados.append({
                "nome": nome,
                "estado": "já existe",
                "id": existente["id"]
            })
            continue

        network = dados.get("network")

        if network:
            canal = network.get("name")
        else:
            web_channel = dados.get("webChannel")
            canal = web_channel.get("name") if web_channel else None

        rating = dados.get("rating") or {}

        imagem = dados.get("image") or {}

        dados_serie = {
            "tvmaze_id": tvmaze_id,
            "nome": dados.get("name"),
            "tipo": dados.get("type"),
            "idioma": dados.get("language"),
            "estado": dados.get("status"),
            "data_estreia": dados.get("premiered"),
            "data_fim": dados.get("ended"),
            "duracao": dados.get("runtime"),
            "classificacao": rating.get("average"),
            "canal": canal,
            "resumo": dados.get("summary"),
            "imagem": imagem.get("original")
        }

        serie_id = inserir_serie(dados_serie)

        for genero in dados.get("genres", []):

            genero_id = obter_ou_criar_genero(genero)

            associar_genero(
                serie_id,
                genero_id
            )

        resultados.append({
            "nome": nome,
            "estado": "importada",
            "id": serie_id
        })

    return resultados