import sys; sys.path.append('..')

from src.app import ContentBasedFiltering
from utils.exporting import convert_to_json_api
from exceptions.error_msg import errorMessageByNotFoundError
from exceptions.exceptions import NotFoundError
from src.fetch_from_sql import connect
from utils.profiling import timeit

@timeit
def Anime():
    conn = connect()
    set_index = 'animeIndex'
    vector = "data/binary/anime_metadata.npy"
    vector1 = "data/binary/animeFeaturesTfidf.npz"
    content = ContentBasedFiltering(vector1=vector, vector2=vector1, dataset='use SQL', index_col=set_index, conn=conn)
    return content

@timeit
def getAnimeById(anime_id) -> dict:
    try:
        content = Anime()
        OriginalsDf, similarDf = content.mostSimilarByIndex(anime_id, n=10)
        return convert_to_json_api(OriginalsDf, similarDf)
    except NotFoundError:
        return errorMessageByNotFoundError(anime_id)
    except ValueError:
        return errorMessageByNotFoundError(anime_id)
    except TypeError:
        return errorMessageByNotFoundError(anime_id)

@timeit
def getnAnimeById(anime_id, n) -> dict:
    try:
        n = int(n)
        content = Anime()
        OriginalsDf, similarDf = content.mostSimilarByIndex(anime_id, n=n)
        return convert_to_json_api(OriginalsDf, similarDf)
    except NotFoundError:
        return errorMessageByNotFoundError(anime_id)
    except ValueError:
        return errorMessageByNotFoundError(anime_id)
    except TypeError:
        return errorMessageByNotFoundError(anime_id)

@timeit
def getAnimeByName(anime_name) -> dict:
    content = Anime()
    OriginalsDf, similarDf = content.mostSimilarByName(anime_name, n=10)
    return convert_to_json_api(OriginalsDf, similarDf)

@timeit
def getnAnimeByName(anime_name, n) -> dict:
    try:
        n = int(n)
        content = Anime()
        OriginalsDf, similarDf = content.mostSimilarByName(anime_name, n=n)
        return convert_to_json_api(OriginalsDf, similarDf)
    except TypeError:
        return errorMessageByNotFoundError(anime_name)

@timeit
def getAnimeName(anime_name) -> dict:
    try:
        content = Anime()
        AnimeDataFrame = content.animeSearch(anime_name, n=1)
        return convert_to_json_api(AnimeDataFrame)
    except TypeError:
        return errorMessageByNotFoundError(anime_name)

@timeit
def getAnimeId(anime_id) -> dict:
    content = Anime()
    AnimeDataFrame = content.animeSearchById(anime_id, n=1)
    return convert_to_json_api(AnimeDataFrame)

@timeit
def getnAnimeName(anime_name, n) -> dict:
    try:
        content = Anime()
        AnimeDataFrame = content.animeSearch(anime_name, n=n)
        return convert_to_json_api(AnimeDataFrame)
    except TypeError:
        return errorMessageByNotFoundError(anime_name)

@timeit
def getnAnimeId(anime_id, n) -> dict:
    content = Anime()
    AnimeDataFrame = content.animeSearchById(anime_id, n=n)
    return convert_to_json_api(AnimeDataFrame)