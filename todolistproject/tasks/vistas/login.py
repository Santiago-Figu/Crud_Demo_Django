import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import jwt
from datetime import datetime, timedelta, timezone
from tasks.models import Usuario
from tasks.utils import AESCipher

@csrf_exempt  # Permite solicitudes POST sin CSRF token (útil para APIs)
def loginview(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        password = request.POST.get('password')

        # Verifica que el correo y la contraseña no estén vacíos
        if not correo or not password:
            return JsonResponse({"error": "Correo y contraseña son obligatorios."}, status=400)

        try:
            cipher = AESCipher(os.getenv("FERNET_KEY"))
            # Busca al usuario por correo
            usuario = Usuario.objects.get(correo=correo)
            
            # Descifra la contraseña almacenada
            password_descifrada = cipher.decrypt(usuario.password)

            # Verifica si la contraseña coincide
            if password == password_descifrada:
                # Genera un token JWT
                payload = {
                    'id': usuario.id,
                    'nombre': usuario.nombre,
                    'correo': correo,
                    'exp':  datetime.now(timezone.utc) + timedelta(minutes=10)
                }
                token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm='HS256')

                # Cifra el token JWT
                token_cifrado = cipher.encrypt(token)

                # Devuelve el token cifrado
                return JsonResponse({"token": token_cifrado}, status=200)
            else:
                return JsonResponse({"error": "Credenciales inválidas."}, status=401)
        except Usuario.DoesNotExist:
            return JsonResponse({"error": "Usuario no encontrado."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método no permitido."}, status=405)