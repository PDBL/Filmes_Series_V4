from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from services.tvmaze_service import pesquisar_series
from services.importacao_service import importar_series
from repositories.series_repository import listar_series, procurar_serie_id
from repositories.genero_repository import listar_generos


app = FastAPI(
    title="Filmes e Séries API",
    description="API para importar séries através da TVmaze API, guardar na base de dados e disponibilizar para consulta.",
    version="4.0.0"
)

app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")   


@app.get("/api/status")
async def status():

    return {
        "estado": "online",
        "api_externa": "TVmaze"
    }


@app.get("/api/series/pesquisar")
async def pesquisar(nome: str):

    if not nome.strip():
        raise HTTPException(
            status_code=400,
            detail="O nome da série é obrigatório."
        )

    try:

        dados = await pesquisar_series(nome)

        return dados

    except Exception:

        raise HTTPException(
            status_code=502,
            detail="Não foi possível obter dados da TVmaze API."
        )


@app.post("/api/series/importar")
async def importar():

    try:

        resultado = await importar_series()

        return {
            "mensagem": "Processo de importação concluído.",
            "series": resultado
        }

    except Exception as erro:

        raise HTTPException(
            status_code=500,
            detail=str(erro)
        )


@app.get("/api/series")
async def obter_series(
    nome: str | None = None,
    genero: str | None = None
):

    try:

        series = listar_series(nome, genero)

        return series

    except Exception as erro:

        raise HTTPException(
            status_code=500,
            detail=str(erro)
        )


@app.get("/api/series/{id_serie}")
async def obter_serie(id_serie: int):

    try:

        serie = procurar_serie_id(id_serie)

        if serie is None:

            raise HTTPException(
                status_code=404,
                detail="Série não encontrada."
            )

        return serie

    except HTTPException:
        raise

    except Exception as erro:

        raise HTTPException(
            status_code=500,
            detail=str(erro)
        )


@app.get("/api/generos")
async def obter_generos():

    try:

        return listar_generos()

    except Exception as erro:

        raise HTTPException(
            status_code=500,
            detail=str(erro)
        )