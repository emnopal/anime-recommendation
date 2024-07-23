def errorMessageByTypeError(anime_id):
    error_msg = "MAL ID: {} not found, please try again or you can check it to MAL for making sure it's available"
    error_msg_solution = "Go to this link: https://myanimelist.net/anime/{}, if that link is broken or not available or 404, so no data is available"

    return {
        'error': error_msg.format(anime_id),
        "solution": error_msg_solution.format(anime_id)
    }


def errorMessageByValueError(anime_id):
    return errorMessageByTypeError(anime_id)


def errorMessageByAttributeError(anime_id):
    return errorMessageByTypeError(anime_id)


def errorMessageByNotFoundError(anime_id):
    return errorMessageByTypeError(anime_id)