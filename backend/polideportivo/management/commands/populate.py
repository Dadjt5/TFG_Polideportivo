import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from polideportivo.models import Administrador, RolAdministrador, Configuracion, Foro

User = get_user_model()


class Command(BaseCommand):
    help = "Carga inicial del sistema"

    def handle(self, *args, **kwargs):

        # Super usuario
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                password=password
            )
            self.stdout.write(self.style.SUCCESS("Superusuario técnico creado"))

        # Usuario admin raiz
        username = os.environ.get("DJANGO_ADMIN_USERNAME")
        email = os.environ.get("CLIENTE_ADMIN_EMAIL", "admin@polideportivo.com")
        password = os.environ.get("DJANGO_ADMIN_PASSWORD")

        if not User.objects.filter(username=username).exists():

            with transaction.atomic():

                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    is_staff=True
                )

                Administrador.objects.create(
                    user=user,
                    nombre="Administrador Principal",
                    DNI=username,
                    rol=RolAdministrador.RAIZ
                )

            self.stdout.write(self.style.SUCCESS("Administrador RAIZ creado"))
        
        # Configuracion del sistema
        if not Configuracion.objects.exists():
            Configuracion.objects.create(
                max_deportes_por_usuario=5,
                dias_minimo_reserva_actividad=1,
                dias_maximo_reserva_actividad=7,
                dias_minimo_cancelacion=1,
                horas_previas_notificacion=2,
                titulo_cambios_cancelaciones="Aviso sobre cancelaciones",
                titulo_avisos_actividades="Nueva actividad",
                titulo_problemas_pago="Fallo en el pago",
                titulo_salida_lista_espera="Salida de la lista de espera",
                titulo_ausencias="Aviso por falta de asistencia",
                titulo_material_especial="Nuevo material especial necesario",
                texto_cambios_cancelaciones="Las cancelaciones deben realizarse con antelación suficiente.",
                texto_avisos_actividades="Hay una nueva actividad que podría interesarle.",
                texto_problemas_pago="Si tiene problemas con el pago contacte con administración.",
                texto_salida_lista_espera="Ha salido de la lista de espera.",
                texto_ausencias="Recuerde justificar sus ausencias.",
                texto_material_especial="Algunas actividades requieren nuevo material."
            )

            self.stdout.write(self.style.SUCCESS("Configuración global creada"))
        else:
            self.stdout.write(self.style.WARNING("La configuración ya existe"))
        
        # Foro unico del sistema
        if not Foro.objects.exists():
            Foro.objects.create(
                titulo = "Foro",
                numeroParticipantes = 0
            )

            self.stdout.write(self.style.SUCCESS("Foro general creado"))
        else:
            self.stdout.write(self.style.WARNING("El foro ya existe"))