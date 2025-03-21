from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from tasks.models import Task
from tasks.serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related('usuario').all()
    serializer_class = TaskSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Task.DoesNotExist:
            return Response(
                {
                    "error": "Datos de la tarea no encontrados",
                    "message": "La tarea solicitada no existe.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )