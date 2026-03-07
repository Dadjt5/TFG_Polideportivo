from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import transaction
from django.contrib.auth import get_user_model

from .usuario import Usuario

class Monitor(Usuario):
    """Modelo para representar al monitor"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="monitor")

    @classmethod
    def registrar_monitor(cls, *, nombre, apellidos, dni, email, password):

        User = get_user_model()

        if User.objects.filter(username=dni).exists():
            return {
                "respuesta": "Ya existe un usuario con ese DNI",
                "error": True
            }

        if User.objects.filter(email=email).exists():
            return {
                "respuesta": "Ya existe un usuario con ese email",
                "error": True
            }

        with transaction.atomic():
            auth_user = User.objects.create_user(
                username=dni,
                email=email,
                password=password
            )

            monitor = cls.objects.create(
                user=auth_user,
                nombre=nombre,
                apellidos=apellidos,
                DNI=dni,
            )

        return {
            "respuesta": monitor,
            "error": False
        }

    @classmethod
    def contar(cls):
        return cls.objects.count()