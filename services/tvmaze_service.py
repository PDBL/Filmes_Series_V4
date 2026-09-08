import httpx


TVMAZE_API_URL = "https://api.tvmaze.com"


async def pesquisar_series(nome: str):

    url = f"{TVMAZE_API_URL}/search/shows"

    params = {
        "q": nome
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    response.raise_for_status()

    return response.json()


async def obter_serie_tvmaze(nome: str):

    url = f"{TVMAZE_API_URL}/singlesearch/shows"

    params = {
        "q": nome
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    if response.status_code == 404:
        return None

    response.raise_for_status()

    return response.json()