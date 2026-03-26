import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from polideportivo.models import Administrador, RolAdministrador, Configuracion, Foro, Canal

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
        else:
            self.stdout.write(self.style.WARNING("Superusuario ya existe"))

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
        else:
            self.stdout.write(self.style.WARNING("Administrador raiz ya existe"))

        # Configuracion del sistema
        if not Configuracion.objects.exists():
            Configuracion.objects.create(
                max_deportes_por_usuario=5,
                dias_minimo_alquiler=0,
                dias_maximo_alquiler=7,
                dias_minimo_cancelacion=1,
                horas_alquiler_consecutivas=2,
                porcentaje_maximo=100,
                titulo_cambios_cancelaciones="Aviso sobre cancelaciones",
                titulo_avisos_actividades="Nueva actividad",
                titulo_problemas_pago="Fallo en el pago",
                titulo_salida_lista_espera="Salida de la lista de espera",
                titulo_ausencias="Aviso por falta de asistencia",
                titulo_material_especial="Nuevo material especial necesario",
                titulo_cambios_sesiones="Cambio en las sesiones",
                texto_cambios_cancelaciones="Los tiempos mínimos de las cancelaciones han cambiado.",
                texto_avisos_actividades="Hay una nueva actividad que podría interesarle.",
                texto_problemas_pago="Si tiene problemas con el pago contacte con administración.",
                texto_salida_lista_espera="Ha salido de la lista de espera.",
                texto_ausencias="Recuerde justificar sus ausencias.",
                texto_material_especial="Algunas actividades requieren nuevo material.",
                texto_cambios_sesiones="Las sesiones de la actividad indicada han cambiado."
            )

            self.stdout.write(self.style.SUCCESS("Configuración global creada"))
        else:
            self.stdout.write(self.style.WARNING("La configuración ya existe"))
        
        # Foro unico del sistema
        if not Foro.objects.exists():
            foro = Foro.objects.create(
                titulo = "Foro",
                numeroParticipantes = 0
            )

            self.stdout.write(self.style.SUCCESS("Foro general creado"))
        else:
            self.stdout.write(self.style.WARNING("El foro ya existe"))
            
        # Canal de sugerencias
        if not Canal.objects.filter(titulo="Buzón de sugerencias").exists():
            Canal.objects.create(
                titulo = "Buzón de sugerencias",
                tema = "Buzón",
                numeroParticipantes = 0,
                secreto=True,
                foro=foro

            )

            self.stdout.write(self.style.SUCCESS("Buzón de sugerencias creado"))
        else:
            self.stdout.write(self.style.WARNING("El buzón de sugerencias ya existe"))
            
        # Buzón de nuevas actividades
        if not Canal.objects.filter(titulo="Nuevas actividades").exists():
            Canal.objects.create(
                titulo = "Nuevas actividades",
                tema = "Proponer nuevas actividades",
                numeroParticipantes = 0,
                secreto=True,
                foro=foro
            )

            self.stdout.write(self.style.SUCCESS("Canal para proponer nuevas actividades creado"))
        else:
            self.stdout.write(self.style.WARNING("El canal de nuevas actividades ya existe"))