from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import RedirectResponse
from api.app import (
    getAnimeById,
    getAnimeByName,
    getAnimeId,
    getAnimeName,
    getnAnimeById,
    getnAnimeByName,
    getnAnimeId,
    getnAnimeName
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/templates/static", StaticFiles(directory="templates/static"), name="templates/static")

# Get Swagger
@app.get("/api")
async def api_docs():
    return RedirectResponse(url='/docs')


# Home
@app.get("/", response_class=HTMLResponse)
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Get anime recommendation
@app.get("/api/recommendations/")
async def get_anime_recommendation(anime_id: int = None, n: int = None, anime_name: str = None):
    if not n:
        if not anime_name:
            return getAnimeById(anime_id=anime_id)
        if not anime_id:
            return getAnimeByName(anime_name=anime_name)
        if not anime_name and not anime_id:
            return {
                "error": "parameter id and name required"
            }
    else:
        if not anime_name:
            return getnAnimeById(anime_id=anime_id, n=n)
        if not anime_id:
            return getnAnimeByName(anime_name=anime_name, n=n)
        if not anime_name and not anime_id:
            return {
                "error": "parameter id and name required"
            }


# Get Anime Database
@app.get("/api/data/")
async def get_anime_name(anime_id: int = None, n: int = None, anime_name: str = None):
    if not n:
        if not anime_name:
            return getAnimeId(anime_id=anime_id)
        if not anime_id:
            return getAnimeName(anime_name=anime_name)
        if not anime_name and not anime_id:
            return {
                "error": "parameter id and name required"
            }
    else:
        if not anime_name:
            return getnAnimeId(anime_id=anime_id, n=n)
        if not anime_id:
            return getnAnimeName(anime_name=anime_name, n=n)
        if not anime_name and not anime_id:
            return {
                "error": "parameter id and name required"
            }


