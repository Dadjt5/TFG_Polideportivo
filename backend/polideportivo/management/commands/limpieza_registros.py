from django.core.management.base import BaseCommand
from datetime import date
from django.db.models import Q
from miapp.models import Alquiler, ReservaActividad, CompraBono, CompraAbono, TDA, Pago, EstadoReserva, EstadoPago

class Command(BaseCommand):
    help = "Elimina registros caducados o cancelados automáticamente"

    def handle(self, *args, **kwargs):
        hoy = date.today()

        # Alquileres caducados o cancelados
        alquileres_qs = Alquiler.objects.filter(Q(fecha__lt=hoy) | Q(estado=EstadoReserva.CANCELADO))
        alquileres_eliminados = alquileres_qs.count()
        alquileres_qs.delete()

        # Actividades canceladas
        actividades_qs = ReservaActividad.objects.filter(estado=EstadoReserva.CANCELADO)
        actividades_eliminadas = actividades_qs.count()
        actividades_qs.delete()

        # Bonos caducados o cancelados
        bonos_qs = CompraBono.objects.filter(Q(fechaExpiracion__lt=hoy) | Q(estado=EstadoReserva.CANCELADO))
        bonos_eliminados = bonos_qs.count()
        bonos_qs.delete()

        # Abonos caducados o cancelados
        abonos_qs = CompraAbono.objects.filter(Q(fechaExpiracion__lt=hoy) | Q(estado=EstadoReserva.CANCELADO))
        abonos_eliminados = abonos_qs.count()
        abonos_qs.delete()

        # TDA caducados o cancelados
        tdas_qs = TDA.objects.filter(Q(fechaExpiracion__lt=hoy) | Q(estado=EstadoReserva.CANCELADO))
        tdas_eliminadas = tdas_qs.count()
        tdas_qs.delete()

        # Pagos cancelados
        pagos_qs = Pago.objects.filter(estadoPago=EstadoPago.CANCELADO)
        pagos_eliminados = pagos_qs.count()
        pagos_qs.delete()

        self.stdout.write(self.style.SUCCESS(
            f"Limpieza completada: {alquileres_eliminados} alquileres, "
            f"{actividades_eliminadas} actividades, "
            f"{bonos_eliminados} bonos, {abonos_eliminados} abonos, "
            f"{tdas_eliminadas} tdas, {pagos_eliminados} pagos eliminados."
        ))