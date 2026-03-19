import uuid
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()

class DNIoCodigoBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        try:
            users = UserModel.objects.filter(
                Q(username=username) | Q(codigo_usuario=username)
            )

            if not users.exists():
                return None

            user = users.first()
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None