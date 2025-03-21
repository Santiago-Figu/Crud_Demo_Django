import os
from dotenv import load_dotenv
from rest_framework import serializers
from .models import Usuario, Task
from .utils import AESCipher
from decouple import config
from django.conf import settings

load_dotenv()
cipher = AESCipher(os.getenv("FERNET_KEY"))


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'created_at', 'usuario']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['usuario'] = UsuarioSerializer(instance.usuario).data  # Serializa el usuario
        return data



class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'apellidos', 'correo','password' ,'telefono']
    

    def validate(self, data):
        """
        Valida que no exista un usuario con el mismo correo.
        """
        correo = data.get('correo')
        if Usuario.objects.filter(correo=correo).exists():
            raise serializers.ValidationError({"correo": "Este correo ya está registrado."})
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            # data['password'] = instance.get_password()
            data['telefono'] = instance.get_telefono()
        except Exception as e:
            print(f"Ocurrio un error al descifrar los datos del usuario: {e}")
        return data

    def to_internal_value(self, data):
        mutable_data = data.copy() # copia de los datos enviados en el post para poder modificarlos
        password = mutable_data.get('password')
        telefono = mutable_data.get('telefono')

        if password:
            mutable_data['password'] = cipher.encrypt(password)

        if telefono:
            mutable_data['telefono'] = cipher.encrypt(telefono)
        
        return super().to_internal_value(mutable_data)