from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def not_found_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # para errores 404
    if response is not None and response.status_code == status.HTTP_404_NOT_FOUND:
        response.data = {
            "error": "Objeto no encontrado",
            "message": "La tarea solicitada no existe.",
            "status_code": response.status_code
        }

    return response