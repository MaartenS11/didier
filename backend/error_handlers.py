from werkzeug.exceptions import NotFound, UnprocessableEntity


def handler_404(e: NotFound):
    return {"error": e.description}, 404


def handler_422(e: UnprocessableEntity):
    print(e)
    print(e.description)
    return {"error": e.description}, 422
