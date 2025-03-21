from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Task, Usuario
from .serializers import TaskSerializer, UsuarioSerializer

# Create your views here.

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related('usuario').all()
    serializer_class = TaskSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Task.DoesNotExist:
            return Response(
                {
                    "error": "Objeto no encontrado",
                    "message": "La tarea solicitada no existe.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )