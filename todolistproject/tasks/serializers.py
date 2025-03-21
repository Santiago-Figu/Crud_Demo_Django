import os
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from dotenv import load_dotenv
from rest_framework import serializers
from .models import Usuario, Task
from .utils import AESCipher, limpiar_caracteres_input, limpiar_input_numerico

load_dotenv()
cipher = AESCipher(os.getenv("FERNET_KEY"))


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'created_at', 'usuario']

    def validate(self, data):
        """
        Valida los datos ingresados por el usuario.
        """
        # Validar que los campos no estén vacíos
        campos_obligatorios = ['title', 'usuario']
        for campo in campos_obligatorios:
            if not data.get(campo):
                raise serializers.ValidationError({campo: "Favor de ingresar un valor."})
            
        data['title'] = limpiar_caracteres_input(data['title'])
   
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # data['usuario'] = UsuarioSerializer(instance.usuario).data  # Serializa el usuario completo
        usuario_data = {
            'id': instance.usuario.id,
            'nombre': instance.usuario.nombre,
            'apellidos': instance.usuario.apellidos
        }
        data['usuario'] = usuario_data
        return data


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'apellidos', 'correo','password' ,'telefono']
    

    def validate(self, data):
        """
        Valida los datos ingresados por el usuario.
        """
        # Validar que los campos no estén vacíos
        campos_obligatorios = ['nombre', 'apellidos', 'correo', 'password', 'telefono']
        for campo in campos_obligatorios:
            if not data.get(campo):
                raise serializers.ValidationError({campo: "Favor de ingresar un valor."})
            
        data['nombre'] = limpiar_caracteres_input(data['nombre'])
        data['apellidos'] = limpiar_caracteres_input(data['apellidos'])
        data['telefono'] = limpiar_input_numerico(data['telefono'])

        # Validar el formato del correo
        try:
            validate_email(data['correo'])
        except DjangoValidationError:
            raise serializers.ValidationError({"correo": "El correo no tiene un formato válido."})

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