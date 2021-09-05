def handler_404(e=None):
    return {"error": e or "The requested resource could not be found."}, 404


def handler_422(e):
    return {"error": e}, 422
