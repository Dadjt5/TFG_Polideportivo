from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()

class DNIoCodigoBackend(ModelBackend):
    """
    Permite autenticarse con username (DNI) o codigo_usuario.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        try:
            user = UserModel.objects.get(
                models.Q(username=username) | models.Q(codigo_usuario=username)
            )
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None