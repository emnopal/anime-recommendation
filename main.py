from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from src.app import ContentBasedFiltering
from utils.exporting import convert_to_json_api
from exceptions.error_msg import errorMessageByNotFoundError
from exceptions.exceptions import NotFoundError


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/templates/static", StaticFiles(directory="templates/static"), name="templates/static")


def getAnime():
    dataset = "data/dataset/anime_clean.csv"
    vector = "data/binary/anime_metadata.npy"
    vector1 = "data/binary/animeFeaturesTfidf.npz"
    return dataset, vector, vector1


# Home
@app.get("/", response_class=HTMLResponse)
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Anime ID, Find most similar anime from MAL (My Anime List) ID
@app.get("/{anime_id}")
@app.get("/id/{anime_id}")
async def anime_by_id(anime_id: int):
    try:
        dataset, vector, vector1 = getAnime()
        content = ContentBasedFiltering(dataset=dataset, vector1=vector, vector2=vector1)  # noqa
        OriginalsDf, similarDf = content.mostSimilarByIndex(anime_id, n=20)
        return convert_to_json_api(OriginalsDf, similarDf)
    except NotFoundError:
        return errorMessageByNotFoundError(anime_id)


@app.get("/{anime_id}/get/{n}")
@app.get("/id/{anime_id}/get/{n}")
async def get_n_anime_by_id(anime_id: int, n: int):
    try:
        n = int(n)
        dataset, vector, vector1 = getAnime()
        content = ContentBasedFiltering(dataset=dataset, vector1=vector, vector2=vector1)  # noqa
        OriginalsDf, similarDf = content.mostSimilarByIndex(anime_id, n=n)
        return convert_to_json_api(OriginalsDf, similarDf)
    except NotFoundError:
        return errorMessageByNotFoundError(anime_id)


# Anime Name, Find most similar anime from name
@app.get("/name/{anime_name}")
async def anime_by_name(anime_name: str):
    dataset, vector, vector1 = getAnime()
    content = ContentBasedFiltering(dataset=dataset, vector1=vector, vector2=vector1)  # noqa
    OriginalsDf, similarDf = content.mostSimilarByName(anime_name, n=20)
    return convert_to_json_api(OriginalsDf, similarDf)


@app.get("/name/{anime_name}/get/{n}")
async def get_n_anime_by_name(anime_name: str, n: int):
    n = int(n)
    dataset, vector, vector1 = getAnime()
    content = ContentBasedFiltering(dataset=dataset, vector1=vector, vector2=vector1)  # noqa
    OriginalsDf, similarDf = content.mostSimilarByName(anime_name, n=n)
    return convert_to_json_api(OriginalsDf, similarDf)
