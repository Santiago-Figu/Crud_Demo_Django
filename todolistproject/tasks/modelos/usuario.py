from django.db import models
from tasks.utils import AESCipher
from django.conf import settings

# Create your models here.

cipher = AESCipher(settings.FERNET_KEY)

class Usuario(models.Model):
    nombre = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    password = models.TextField(default=None)
    correo = models.TextField(max_length=255)
    telefono = models.TextField()

    def set_password(self, password):
        self.correo = cipher.encrypt(password)

    def get_password(self):
        return cipher.decrypt(self.password)

    def set_telefono(self, telefono):
        self.telefono = cipher.encrypt(telefono)
        

    def get_telefono(self):
        return cipher.decrypt(self.telefono)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"
    