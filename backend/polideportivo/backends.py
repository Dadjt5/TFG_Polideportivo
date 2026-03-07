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
            uuid_obj = uuid.UUID(username)
            query = Q(username=username) | Q(codigo_usuario=uuid_obj)

        except ValueError:
            query = Q(username=username)

        try:
            user = UserModel.objects.get(query)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None