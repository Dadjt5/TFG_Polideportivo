from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):

    @property
    def is_usuario_final(self):
        return hasattr(self, 'usuariofinal')

    @property
    def is_monitor(self):
        return hasattr(self, 'monitor')

    @property
    def is_administrador(self):
        return hasattr(self, 'administrador')