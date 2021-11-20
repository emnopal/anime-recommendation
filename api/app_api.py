import sys; sys.path.append('..')

from src.app import ContentBasedFiltering
from utils.exporting import convert_to_json_api
from exceptions.error_msg import errorMessageByNotFoundError
from exceptions.exceptions import NotFoundError


def getAnime():
    dataset = "data/dataset/anime_clean.csv"
    vector = "data/binary/anime_metadata.npy"
    vector1 = "data/binary/animeFeaturesTfidf.npz"
    return dataset, vector, vector1

def Anime():
    dataset, vector, vector1 = getAnime()
    content = ContentBasedFiltering(dataset=dataset, vector1=vector, vector2=vector1)  # noqa
    return content

def getAnimeById(anime_id):
    try:
        content = Anime()
        OriginalsDf, similarDf = content.mostSimilarByIndex(anime_id, n=20)
        return convert_to_json_api(OriginalsDf, similarDf)
    except NotFoundError:
        return errorMessageByNotFoundError(anime_id)

def getnAnimeById(anime_id, n):
    try:
        n = int(n)
        content = Anime()
        OriginalsDf, similarDf = content.mostSimilarByIndex(anime_id, n=n)
        return convert_to_json_api(OriginalsDf, similarDf)
    except NotFoundError:
        return errorMessageByNotFoundError(anime_id)

def getAnimeByName(anime_name):
    content = Anime()
    OriginalsDf, similarDf = content.mostSimilarByName(anime_name, n=20)
    return convert_to_json_api(OriginalsDf, similarDf)

def getnAnimeByName(anime_name, n):
    n = int(n)
    content = Anime()
    OriginalsDf, similarDf = content.mostSimilarByName(anime_name, n=n)
    return convert_to_json_api(OriginalsDf, similarDf)

def getAnimeName(anime_name):
    content = Anime()
    AnimeDataFrame = content.animeSearch(anime_name, n=1)
    return convert_to_json_api(AnimeDataFrame)

def getAnimeId(anime_id):
    content = Anime()
    AnimeDataFrame = content.animeSearchById(anime_id, n=1)
    return convert_to_json_api(AnimeDataFrame)

def getnAnimeName(anime_name, n):
    content = Anime()
    AnimeDataFrame = content.animeSearch(anime_name, n=n)
    return convert_to_json_api(AnimeDataFrame)

def getnAnimeId(anime_id, n):
    content = Anime()
    AnimeDataFrame = content.animeSearchById(anime_id, n=n)
    return convert_to_json_api(AnimeDataFrame)