def errorMessageByTypeError(anime_id):
    return {
            'error': f"MAL ID: {anime_id} not found, please try again or you can check it to MAL for making sure it's available",
            "solution": f"Go to this link: https://myanimelist.net/anime/{anime_id}, if that link is broken or not available or 404, so no data is available"
        }

def errorMessageByValueError(anime_id):
    return {
            'error': f"MAL ID: {anime_id} not found, please try again or you can check it to MAL for making sure it's available",
            "solution": f"Go to this link: https://myanimelist.net/anime/{anime_id}, if that link is broken or not available or 404, so no data is available"
        }

def errorMessageByAttributeError(anime_id):
    return {
            'error': f"MAL ID: {anime_id} not found, please try again or you can check it to MAL for making sure it's available",
            "solution": f"Go to this link: https://myanimelist.net/anime/{anime_id}, if that link is broken or not available or 404, so no data is available"
        }

def errorMessageByNotFoundError(anime_id):
    return {
            'error': f"MAL ID: {anime_id} not found, please try again or you can check it to MAL for making sure it's available",
            "solution": f"Go to this link: https://myanimelist.net/anime/{anime_id}, if that link is broken or not available or 404, so no data is available"
        }