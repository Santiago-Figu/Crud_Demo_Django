from django.db import models

from tasks.modelos.usuario import Usuario

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tareas', default=1)

    class Meta:
        db_table = 'tasks'  # Nombre de la tabla en la base de datos
        app_label = 'tasks'

    def __str__(self):
        return self.title