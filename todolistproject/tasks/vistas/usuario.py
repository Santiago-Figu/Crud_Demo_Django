from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from tasks.models import Usuario
from tasks.serializers import UsuarioSerializer

# Create your views here.

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Usuario.DoesNotExist:
            return Response(
                {
                    "error": "Usuario no encontrado",
                    "message": "El usuario no se encuentra registrado en la base de datos.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )