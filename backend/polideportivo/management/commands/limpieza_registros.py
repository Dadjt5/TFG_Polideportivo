from django.core.management.base import BaseCommand
from datetime import date
from django.db.models import Q

from miapp.models import (
    Alquiler, ReservaActividad, CompraBono,
    CompraAbono, TDA, Pago, EstadoReserva, EstadoPago
)

class Command(BaseCommand):
    help = "Marca como cancelados los registros caducados del sistema"

    def handle(self, *args, **kwargs):
        hoy = date.today()

        # ALQUILERES caducados
        alquileres = Alquiler.objects.filter(fecha__lt=hoy, estado=EstadoReserva.CONFIRMADO)
        alquileres.update(estado=EstadoReserva.CANCELADO)

        # ACTIVIDADES caducadas (por fecha de actividad si tienes)
        actividades = ReservaActividad.objects.filter(
            fecha__lt=hoy,
            estado=EstadoReserva.CONFIRMADO
        )
        actividades.update(estado=EstadoReserva.CANCELADO)

        # BONOS caducados
        bonos = CompraBono.objects.filter(
            fechaExpiracion__lt=hoy,
            estado=EstadoReserva.CONFIRMADO
        )
        bonos.update(estado=EstadoReserva.CANCELADO)

        # ABONOS caducados
        abonos = CompraAbono.objects.filter(
            fechaExpiracion__lt=hoy,
            estado=EstadoReserva.CONFIRMADO
        )
        abonos.update(estado=EstadoReserva.CANCELADO)

        # TDA caducados
        tdas = TDA.objects.filter(
            fechaExpiracion__lt=hoy,
            estado=EstadoReserva.CONFIRMADO
        )
        tdas.update(estado=EstadoReserva.CANCELADO)

        # PAGOS asociados a reservas canceladas
        pagos = Pago.objects.filter(
            estadoPago=EstadoPago.PENDIENTE
        ).filter(
            Q(content_type__model='alquiler', object_id__in=alquileres.values('id')) |
            Q(content_type__model='reservactividad', object_id__in=actividades.values('id'))
        )

        pagos.update(estadoPago=EstadoPago.CANCELADO)

        self.stdout.write(self.style.SUCCESS(
            "Limpieza completada: elementos caducados marcados como CANCELADO correctamente."
        ))