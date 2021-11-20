from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import RedirectResponse
from api.app_api import *



app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/templates/static", StaticFiles(directory="templates/static"), name="templates/static")


# Home
@app.get("/", response_class=HTMLResponse)
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api")
async def api_docs():
    return RedirectResponse(url='/docs')


# Anime ID, Find most similar anime from MAL (My Anime List) ID
@app.get("/api/recommendations/{anime_id}")
@app.get("/api/recommendations/id/{anime_id}")
async def anime_by_id(anime_id: int):
    return getAnimeById(anime_id=anime_id)


@app.get("/api/recommendations/{anime_id}/get/{n}")
@app.get("/api/recommendations/id/{anime_id}/get/{n}")
async def get_n_anime_by_id(anime_id: int, n: int):
    return getnAnimeById(anime_id=anime_id, n=n)


# Anime Name, Find most similar anime from name
@app.get("/api/recommendations/name/{anime_name}")
async def anime_by_name(anime_name: str):
    return getAnimeByName(anime_name=anime_name)


@app.get("/api/recommendations/name/{anime_name}/get/{n}")
async def get_n_anime_by_name(anime_name: str, n: int):
    return getnAnimeByName(anime_name=anime_name, n=n)


# Get Anime DataFrame
# Get Anime name
@app.get("/api/data/name/{anime_name}")
async def anime_name(anime_name: str):
    return getAnimeName(anime_name=anime_name)

# Get Anime id
@app.get("/api/data/{anime_id}")
@app.get("/api/data/id/{anime_id}")
async def anime_name(anime_id: int):
    return getAnimeId(anime_id=anime_id)

# Get Anime name
@app.get("/api/data/name/{anime_name}/get/{n}")
async def anime_name(anime_name: str, n: int):
    return getnAnimeName(anime_name=anime_name, n=n)

# Get Anime id
@app.get("/api/data/{anime_id}/get/{n}")
@app.get("/api/data/id/{anime_id}/get/{n}")
async def anime_name(anime_id: int, n: int):
    return getnAnimeId(anime_id=anime_id, n=n)
